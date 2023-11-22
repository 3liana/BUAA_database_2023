
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

export function setAvatar(params) {
	var data = new FormData();
	data.append("username", params.username);
	data.append("photo", params.username);
	return post('/api/setAvatar', data);
}

export function getAvatar(username) {
	return get('/api/getAvatar/'+`${username}`);
}

export function logout() {
	var data = new FormData();
	return post('/api/logout', data);
}

export function createPost(params) {
	var data = new FormData();
	data.append("username", params.username);
	console.log(params.username);
	data.append("title", params.title);
	data.append("content", params.content);
	
	return post('/api/createPost', data);
}

export function getPost(post_id) {
	var data = new FormData();
	data.append("post_id" , post_id);
	return post('/api/getPost', data);
}

export function getAllPosts() {
	return post('/api/getAllPosts', new FormData());
}

