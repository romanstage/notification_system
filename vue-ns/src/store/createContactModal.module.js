const initialState = {
    createContact: {
        dialog: false,
        contact: {
            mobile_phone: [],
        },
    }
};

export const createContactModal = {
  namespaced: true,
  state: initialState,
  actions: {
    openDialogCreateContact({ commit }) {
       commit('openDialogCreateContactSuccess');
    },
    closeDialogCreateContact({ commit }) {
      commit('closeDialogCreateContactSuccess');
    },
    addPhoneNumber({ commit }, number) {
      commit('addPhoneNumberSuccess', number);
    },
    removePhoneNumber({ commit }, numberIndex) {
      commit('removePhoneNumberSuccess', numberIndex);
    },
    clearPhoneNumber({ commit }) {
      commit('clearPhoneNumberSuccess',);
    }

  },
  mutations: {
    openDialogCreateContactSuccess(state) {
      state.createContact.dialog = true;
    },
    closeDialogCreateContactSuccess(state) {
      state.createContact.dialog = false;
    },
    addPhoneNumberSuccess(state, number) {
        state.createContact.contact.mobile_phone.push(number);
    },
    clearPhoneNumberSuccess(state) {
        state.createContact.contact.mobile_phone = [];
    },
    removePhoneNumberSuccess(state, number) {
        console.log('remove from store');
        console.log(number);
        var numbers = state.createContact.contact.mobile_phone.filter(function( obj ) {
          return obj !== number;
        });
        console.log(numbers);
        state.detailModal.contact.mobile_phone = numbers;
    },
  }
};