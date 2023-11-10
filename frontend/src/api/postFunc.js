import { post, get} from './api';
export function inviteUserIntoChatGroup(params){
	var data=new FormData();
	data.append("name",params.name);
	data.append("password",params.password);
    data.append("phone",params.phone);
	data.append("wehcat",params.wechat);
	console.log(params);
	return post('/api/register/',data);
}

export function userLogin(params) {
    var data=new FormData();
	data.append("name",params.name);
	data.append("password",params.password);
	
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

