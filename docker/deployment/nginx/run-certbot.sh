#!/bin/bash

# Source in util.sh so we can have our nice tools
. $(cd $(dirname $0); pwd)/util.sh

auto_enable_configs
supervisorctl start nginx

while : ; do
    ps aux | grep nginx | grep -q -v grep
    if [ $? -eq 0 ]; then
        break
    fi
done

exit_code=0
# Loop over every domain we can find
for domain in $(parse_domains); do
    if is_renewal_required $domain; then
        extra_domains=$(parse_extra_domains $domain)
        renewal_domains="$domain $extra_domains"
        # Renewal required for this doman.
        # Last one happened over a week ago (or never)
        if ! get_certificate "$renewal_domains" "isd.apiteam@ucl.ac.uk"; then
            error "Cerbot failed for $renewal_domain. Check the logs for details."
            exit_code=1
        fi
        
        # After trying to get all our certificates, auto enable any configs that we
        # did indeed get certificates for

        auto_enable_configs
        supervisorctl restart nginx
    else
        echo "Not run certbot for $domain; last renewal happened just recently."
    fi
done


set +x
exit $exit_code