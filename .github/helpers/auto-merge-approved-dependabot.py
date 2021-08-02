# Auto Merge Approved Dependencies
#
# This is a simple script to automate the merging of approved dependabot pull requests, it utilises
# github cli.
#

import subprocess
import json
from time import sleep, time


def wrap_subprocess(cmd):
    run_result = subprocess.run(cmd, capture_output=True)
    if run_result.returncode != 0:
        print(run_result.stdout)
        print(run_result.stderr)
        raise subprocess.CalledProcessError

    return run_result


def request_authorised_dependabot():
    prs = wrap_subprocess(
        ['gh', 'pr', 'list', '--search', 'author:app/dependabot review:approved', '--json', 'number,title'])

    prs_dict = json.loads(prs.stdout)
    prs_dict.sort(key=lambda x: x['number'])
    return prs_dict


def is_pr_behind(pr):
    try:
        merge_state = wrap_subprocess(['gh', 'pr', 'view', str(pr), '--json', 'mergeStateStatus'])
        merge_state_dict = json.loads(merge_state.stdout)
        return merge_state_dict['mergeStateStatus'] == 'BEHIND'
    except subprocess.CalledProcessError as exception:
        print(merge_state.stdout)
        print(merge_state.stderr)
        raise exception


def pretty_time_delta(seconds):
    seconds = int(seconds)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    if hours > 0:
        return '%dh%dm%ds' % (hours, minutes, seconds)
    elif minutes > 0:
        return '%dm%ds' % (minutes, seconds)
    else:
        return '%ds' % (seconds, )


ci_time = 60
count = 0
requests = request_authorised_dependabot()

while len(requests) > 0:
    print(len(requests), 'remaining')
    print('Rebasing', requests[0]['title'])

    number = requests[0]['number']

    # Ensure auto merge is enabled
    auto_merge = wrap_subprocess(['gh', 'pr', 'merge', str(number), '--auto', '--squash'])

    # Rebase with dependabot
    if is_pr_behind(number):
        comment = wrap_subprocess(['gh', 'pr', 'comment', str(number), '-b', '@dependabot rebase'])

    start = time()
    sleep(ci_time)
    success = True

    # TODO(low): ideally we would also check for a failure in GitHub actions, however currently this is not possible
    # with gh in a method which works cross platform.
    while len(list(filter(lambda x: x['number'] == number, requests))):
        if is_pr_behind(number):
            success = False
            break
        sleep(30)
        requests = request_authorised_dependabot()

    if not success:
        print('Another PR has been merged ahead of this one, retrying')
        continue
    ci_time = ((ci_time * count) + (time() - start)) / (count + 1) - 30
    count += 1
    print('Merged', number)
    print('Estimated:', pretty_time_delta(ci_time * len(requests)))

print('Merged all dependabot pull requests')
