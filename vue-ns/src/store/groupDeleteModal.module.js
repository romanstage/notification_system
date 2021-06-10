const initialState = {
    deleteModal: {
        dialog: false,
        contact: {
            id: null,
            title: null,
        },
    }

};

export const groupDeleteModal = {
  namespaced: true,
  state: initialState,
  actions: {
    openGroupDeleteModal({ commit }, contact) {
        console.log('GroupDeteleModal action ')
       commit('openGroupDeleteModalSuccess', contact);

    },
    closeGroupDeleteModal({ commit }) {
      commit('closeGroupDeleteModalSuccess');
    },
  },
  mutations: {
    openGroupDeleteModalSuccess(state, contact) {
        console.log('GroupDeteleModal mut ')
      state.deleteModal.dialog = true;
      state.deleteModal.contact = contact;
    },
    closeDialogDetailSuccess(state) {
      state.deleteModal.dialog = false;
      state.deleteModal.contact = {
            id: null,
            title: null
        };
    },
  }
};