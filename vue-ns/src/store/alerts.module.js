const initialState = {
    alerts: [],
};

export const alerts = {
  namespaced: true,
  state: initialState,
  actions: {
    addAlert({ commit }, alert) {
        commit('addAlertSuccess', alert);
        setTimeout(() => {
        commit('removeAlert');
        }, 3000);
    },
  },
  mutations: {
        addAlertSuccess(state, alert) {
        console.log('MUTATION');
        if (state.alerts.length === 6) {
            state.alerts.shift();
        }
        state.alerts.push(alert);
        console.log(state.alerts)
        },
        removeAlert(state) {
            state.alerts.shift();
    },
  }
};