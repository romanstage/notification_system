import axios from 'axios';
import authHeader from './auth-header';

const API_URL = 'http://localhost:8080/api/';

class UserService {
  getUserInfo() {
    return axios.get(API_URL + 'user_info/', { headers: authHeader() });
  }
}

export default new UserService();