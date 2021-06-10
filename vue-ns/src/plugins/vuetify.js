import Vue from 'vue';
import Vuetify from 'vuetify/lib';

Vue.use(Vuetify);

// Translation provided by Vuetify (javascript)
import ru from 'vuetify/es5/locale/ru'

export default new Vuetify({
     lang: {
        locales: { ru, },
        current: 'ru',
      },
});
