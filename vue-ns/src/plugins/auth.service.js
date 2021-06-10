import axios from './api.service';
import authHeader from '@/plugins/auth-header'
import jwt_decode from 'jwt-decode'
import Vue from "vue";

const API_URL = '/api/token/';


class AuthService {
    login(user) {
        console.log('SEND AXIOS')
        console.log(user)
        return axios
            .post(API_URL, {
                username: user.username,
                password: user.password
            })
            .then(response => {
                console.log('RESPONSE OK')
                console.log(response)
                var userFromBack = {};
                if (response.data) {
                    console.log('DATA OK');
                    var decoded = jwt_decode(response.data.access);
                    console.log(decoded);
                    userFromBack = {
                        'user_id': decoded.user_id, 'first_name': decoded.first_name,
                        'last_name': decoded.last_name, 'groups': decoded.groups,
                        'exp': decoded.exp
                    };
                    console.log('USER CRATE OK');
                    localStorage.setItem('access', response.data.access);
                    localStorage.setItem('refresh', response.data.refresh);
                    localStorage.setItem('user', JSON.stringify(userFromBack));
                    console.log('STORE IN LOCAL OK');
                    axios.defaults.headers.common['Authorization'] = 'JWT ' + response.data.access;
                } else {
                    userFromBack = null
                }

                return userFromBack;
            });
    }


    logout() {
        localStorage.removeItem('access');
        localStorage.removeItem('refresh');
        localStorage.removeItem('user');
    }

    refresh() {
        return axios.post(API_URL + 'refresh/',
            {
                "refresh": localStorage.getItem('refresh')
            })
            .then(res => {
                console.log(res);
                console.log(status);
                var userFromBack = {};
                if (res.status === 200) {
                    console.log('REFRESH TOKEN SUCCESS')
                    // 1) put token to LocalStorage
                    localStorage.setItem('access', res.data.access);
                    localStorage.setItem('refresh', res.data.refresh);
                    var decoded = jwt_decode(res.data.access);

                    userFromBack = {
                        'user_id': decoded.user_id, 'first_name': decoded.first_name,
                        'last_name': decoded.last_name, 'groups': decoded.groups,
                        'exp': decoded.exp
                    };
                    localStorage.setItem('user', JSON.stringify(userFromBack));
                    // 2) Change default Authorization header and original request
                    axios.defaults.headers.common['Authorization'] = 'JWT ' + res.data.access;
                }
                return userFromBack;
            });


    }
}

export default new AuthService();
