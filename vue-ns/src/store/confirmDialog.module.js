const initialState = {
    confirmDialog: {
        dialog: false,
        message: {
            title: null,
            message: null,
            confirmMessage: null,
            cancelMessage: null,
            onSubmit: null,
        },
    }
};

export const dialog = {
  namespaced: true,
  state: initialState,
  actions: {
    openDialog({ commit }, message) {
       commit('openDialogSuccess', message);
    },
    closeDialog({ commit }) {
      commit('closeDialogSuccess');
    },
  },
  mutations: {
    openDialogSuccess(state, message) {
      console.log('MUTATION')
      state.confirmDialog.dialog = true;
      state.confirmDialog.message = message;
      console.log(state.confirmDialog)
    },
    closeDialogSuccess(state) {
        console.log('dispath suc')
      state.confirmDialog.dialog = false;
      state.confirmDialog.message = {
            title: null,
            message: null,
            confirmMessage: null,
            cancelMessage: null,
            onSubmit: null,
        };
    },
  }
};