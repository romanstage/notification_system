//Contact list

import axios from "axios";
import store from "../store";
import router from "../router";

const token = localStorage.getItem('access')
if (token) {
  axios.defaults.headers.common['Authorization'] = 'JWT ' + token
}
// axios.defaults.baseURL = 'http://172.21.128.50:8000'
// axios.defaults.baseURL = 'http://127.0.0.1:8000'
axios.defaults.baseURL = 'http://172.21.128.124:8000'

axios.interceptors.response.use((response) => {
                return response
            }, error => {

                const originalRequest = error.config;
                const refreshURL = '/api/token/refresh/';
                if (error.response.status === 401 && !originalRequest._retry
                    && error.response.data.detail === 'Given token not valid for any token type'
                ) {
                    console.log('CATCH TIMEOUT TOKEN')
                    originalRequest._retry = true;
                    axios.post(refreshURL,
                        {
                            "refresh": localStorage.getItem('refresh')
                        })
                        .then(res => {
                            console.log(res);
                            console.log(status);
                            if (res.status === 200) {
                                console.log('REFRESH TOKEN SUCCESS')
                                // 1) put token to LocalStorage
                                localStorage.setItem('access', res.data.access);
                                localStorage.setItem('refresh', res.data.refresh);
                                // 2) Change default Authorization header and original request
                                axios.defaults.headers.common['Authorization'] = 'JWT ' + res.data.access;
                                originalRequest.headers.Authorization = 'JWT ' + res.data.access;
                                // console.log(originalRequest);

                                // 3) return originalRequest object with Axios.
                                return axios(originalRequest);
                            }
                        })
                }
                else if (error.response.status === 403
                ) {
                    this.router.push('/access-denied').catch(()=>{});
                }
                else if (error.response.status === 500 || error.response.status === 404
                ) {
                    this.router.push('/server-error').catch(()=>{});
                }
                else {
                    console.log('NOT VALID TOKEN, LOGOUT');
                    store.dispatch("auth/logout");
                    router.push('/login').catch(()=>{});
                }
                // return Error object with Promise
                return Promise.reject(error);
});

export default axios
