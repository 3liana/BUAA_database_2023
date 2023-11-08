import { post, get} from './api';
export function inviteUserIntoChatGroup(name,password,phone,wechat){
	var data=new FormData();
	data.append("name",name);
	data.append("password",password);
    data.append("phone",phone);
	data.append("wehcat",wechat);
	return post('/api/register/',data);
}

export function userLogin(name, password) {
    var data=new FormData();
	data.append("name",name);
	data.append("password",password);
	return post('/api/login/',data);
}

export function setAvator(user, photo) {
	var data = new FormData();
	data.append("user", user);
	data.append("photo", photo);
	return post('/api/setAvatar', data);
}

export function getAvator(user) {
	return get('/api/getAvatar/'+`${user}`);
}

export function logout() {
	var data = new FormData();
	return post('/api/logout', data);
}

