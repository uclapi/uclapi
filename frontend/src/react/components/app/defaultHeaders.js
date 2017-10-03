import Cookies from 'js-cookie';

export default {
  'Content-Type': 'application/x-www-form-urlencoded',
  'X-CSRFToken': Cookies.get('csrftoken')
};
