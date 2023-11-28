import Vue from 'vue'
import Vuex from 'vuex'
import user from './user'
import snack from './snack'

Vue.use(Vuex)

const getters = {
  snackShow: state => state.snack.snackShow,
  snackMsg: state => state.snack.snackMsg,
  snackType: state => state.snack.snackType
}

export default new Vuex.Store({
  state: {
  },

  mutations: {
  },
  actions: {
  },
  modules: {
    user,
    snack
  },
  getters
})
