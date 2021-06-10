const initialState = {
    genericModal: {
        dialog: false,
        message: null,
    }
};

export const genericModal = {
  namespaced: true,
  state: initialState,
  actions: {
    openGenericModal({ commit }, message) {
        console.log('genericModal action ', 'message')
       commit('openGenericModalSuccess', message);

    },
    closeGenericModal({ commit }) {
      commit('closeGenericModalSuccess');
    },
  },
  mutations: {
    openGenericModalSuccess(state, message) {
        console.log('genericModal mutation ')
      state.genericModal.dialog = true;
      state.genericModal.message = message;
    },
    closeGenericModalSuccess(state) {
      state.genericModal.dialog = false;
      state.genericModal.message = null;
    },
  }
};