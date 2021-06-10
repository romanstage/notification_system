import AuthService from '../plugins/auth.service';

const user = JSON.parse(localStorage.getItem('user'));
function initialState() {
    var loggedInInit = false;
    var haveGroupInit = false;
    var multiGroupInit = false;
    var userInit = null;
    if (user) {
        userInit = user;
        loggedInInit = true;
        if (user.groups.length < 1) {

            haveGroupInit = false
            multiGroupInit = false
          }
          else if (user.groups.length === 1) {
            haveGroupInit = true
            multiGroupInit = false
          }
          else if (user.groups.length > 1) {
             haveGroupInit = true
            multiGroupInit = true
          }


    }
    const initState = {

      status: {
        loggedIn: loggedInInit,
        haveGroup: haveGroupInit,
        multiGroup: multiGroupInit,
      },
      user: userInit,
    }
    return initState
};
// const initialState = user
//   ? { status: { loggedIn: true, haveGroup: false, multiGroup: false, }, user }
//   : { status: { loggedIn: false, haveGroup: false, multiGroup: false, }, user: null };

export const auth = {
  namespaced: true,
  state: initialState,
  actions: {
    login({ commit, dispatch }, user) {
      return AuthService.login(user).then(
        user => {
          console.log('LOGIN OK RUNN COMMIT')
          console.log(user)
          commit('loginSuccess', user);
          const now = Date.now() / 1000;
          let timeUntilRefresh = user.exp - now;
          timeUntilRefresh -= 5 // Refresh 5 seconds before it expires
          console.log(timeUntilRefresh)
          setTimeout(() => dispatch('refresh'), timeUntilRefresh*1000);
          return Promise.resolve(user);
        },
        error => {
          commit('loginFailure');
          return Promise.reject(error);
        }
      );
    },
    logout({ commit }) {
      AuthService.logout();
      commit('logout');
    },
    refresh({ commit, dispatch }) {
      AuthService.refresh().then(
        user => {
          console.log('REFRESH OK RUNN COMMIT')
          console.log(user)
          commit('refreshSuccess', user);
          const now = Date.now() / 1000;
          let timeUntilRefresh = user.exp - now;
          timeUntilRefresh -= 5 // Refresh 5 seconds before it expires
          console.log(timeUntilRefresh)
          setTimeout(() => dispatch('refresh'), timeUntilRefresh*1000);
          return Promise.resolve(user);
        },
        error => {
          commit('loginFailure');
          return Promise.reject(error);
        }
      );

    },

  },
  mutations: {
    loginSuccess(state, user) {
      console.log('MUTATION')
      console.log(user)
      state.status.loggedIn = true;
      state.user = user;

      if (user.groups.length < 1) {
         console.log('no group')
        state.status.haveGroup = false
        state.status.multiGroup = false
      }
      else if (user.groups.length === 1) {
        console.log('one group')
        state.status.haveGroup = true
        state.status.multiGroup = false
      }
      else if (user.groups.length > 1) {
         console.log('multi group')
        state.status.haveGroup = true
        state.status.multiGroup = true
      }



    },
    loginFailure(state) {
      state.status.loggedIn = false;
      // state.status.haveGroup = false
      // state.status.multiGroup = false
      state.user = null;
    },
    logout(state) {
      state.status.loggedIn = false;
      state.status.haveGroup = false
      state.status.multiGroup = false
      state.user = null;

    },
    refreshSuccess(state, user) {
      console.log('MUTATION')
      console.log(user)
      state.status.loggedIn = true;
      state.user = user;

      if (user.groups.length < 1) {
         console.log('no group')
        state.status.haveGroup = false
        state.status.multiGroup = false
      }
      else if (user.groups.length === 1) {
        console.log('one group')
        state.status.haveGroup = true
        state.status.multiGroup = false
      }
      else if (user.groups.length > 1) {
         console.log('multi group')
        state.status.haveGroup = true
        state.status.multiGroup = true
      }

    },

  }
};