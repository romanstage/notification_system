const initialState = {
    detailModal: {
        dialog: false,
        contact: {
            id: null,
            cn: null,
        },
    }
};

export const contactDetailModal = {
  namespaced: true,
  state: initialState,
  actions: {
    openDialogDetail({ commit }, contact) {
       commit('openDialogDetailSuccess', contact);
    },
    closeDialogDetail({ commit }) {
      commit('closeDialogDetailSuccess');
    },
    addPhoneNumber({ commit }, number) {
      commit('addPhoneNumberSuccess', number);
    },
    removePhoneNumber({ commit }, numberIndex) {
      commit('removePhoneNumberSuccess', numberIndex);
    }

  },
  mutations: {
    openDialogDetailSuccess(state, contact) {
      console.log('MUTATION')
      state.detailModal.dialog = true;
      state.detailModal.contact = contact;
    },
    closeDialogDetailSuccess(state) {
      state.detailModal.dialog = false;
      state.detailModal.contact = {
            id: null,
            cn: null,
        };
    },
    addPhoneNumberSuccess(state, number) {
        state.detailModal.contact.mobile_phone.push(number);
    },
    removePhoneNumberSuccess(state, number) {
        console.log('remove from store');
        console.log(number);
        var numbers = state.detailModal.contact.mobile_phone.filter(function( obj ) {
          return obj !== number;
        });
        console.log(numbers);
        state.detailModal.contact.mobile_phone = numbers;
    },
  }
};