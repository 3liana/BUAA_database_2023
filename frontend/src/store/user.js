import { int2Role } from "@/components/role";
import { da } from "element-plus/es/locale";

const keyName = 'loginInfo';

let initial = null;

try {
    initial = parse(localStorage.getItem(keyName));
} catch (e) {
    console.log("Unable to get session data: " + String(e))
}

const user = {
    namespace: true,
    state: {
        loginInfo: initial,
    },
    mutations: {
        setInfo(state, data) {
            state.loginInfo = data.info
        },
        setName(state, name) {
            state.loginInfo.username = name;
            localStorage.setItem(keyName,JSON.stringify(state.loginInfo));
        },
        setAvatar(state, avatar) {
            state.loginInfo.avatar = avatar;
            localStorage.setItem(keyName,JSON.stringify(state.loginInfo));
        }
    },
    actions: {
        login({ commit }, {info,remember}) {
            commit('setInfo', {info,remember})
            localStorage.setItem(keyName,JSON.stringify(info))
        },
        logout({ commit }) {
            localStorage.removeItem(keyName)
            commit('setInfo', {info: null})
        }
    },
    getters: {
        loggedIn: state => state.loginInfo !== null,
        id: state => state.loginInfo?.userId,
        name: state => state.loginInfo?.username,
        role: state => state.loginInfo? int2Role.find(tmp => tmp.value === state.loginInfo.role).role : null,
        avatar: state => (state.loginInfo && state.loginInfo.avatar) ? state.loginInfo.avatar:"https://randomuser.me/api/portraits/women/81.jpg",
        
    },
}