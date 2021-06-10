// функция обновления хэдера
export default function authHeader() {
  let access = JSON.parse(localStorage.getItem('access'));

  if (access) {
    console.log('UPDATE HEDER')
    return { Authorization: 'JWT ' + access };
  } else {
    return {};
  }
}