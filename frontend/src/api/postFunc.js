
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

export function changePassWord(params) {
	var data = new FormData();
	data.append("username", params.username);
	data.append("new_password", params.password);
	console.log(params);
	return post('/api/changePassword', data);
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
	console.log(post_id);
	data.append("post_id" , post_id);
	return post('/api/getPost', data);
}

export function getAllPosts() {
	return post('/api/getAllPosts', new FormData());
}

export function getPostCommodities(post_id) {
	var data = new FormData();
	data.append("post_id", post_id);
	return post('/api/getPostCommodities', data);
}

export function createOrder(params){
	var data = new FormData();
	data.append("username", params.username);
	data.append("commodity_id", params.commodity_id);
	return post('/api/createOrder', data);

}

export function createCommodity(params) {
	var data = new FormData();
	data.append("name", params.name);
	data.append("dc", params.dc);
	data.append("price", params.price);
	data.append("post_id", params.post_id);
	return post('/api/createCommodity', data);

}

export function addCommodityPicture(params) {
	var data = new FormData();
	data.append("commodity_id", params.commodity_id);
	data.append("photo", params.photo);
	return post('/api/addCommodityPicture', data);

}

export function getCommodityPictures(commodity_id) {
	var data = new FormData();
	data.append("commodity_id", commodity_id);
	return post('/api/getCommodityPictures', data);
}

export function deletePost(post_id) {
	var data = new FormData();
	data.append("post_id", post_id);
	return post('/api/deletePost', data);
}

export function changePost(params) {
	var data = new FormData();
	data.append("post_id", params.post_id);
	data.append("title", params.title);
	data.append("content", params.content);
	return post('/api/changePost', data);

}

export function checkIfOrdered(commodity_id) {
	var data = new FormData();
	data.append("commodity_id", commodity_id);
	return post('/api/checkIfOrdered', data);
}

export function allTags() {
	return post('/api/allTags', new FormData());
}

export function getPostTags(post_id) {
	var data = new FormData();
	data.append("post_id", post_id);
	//console.log(String(post_id));
	return post('/api/getPostTags', data);
}

export function getTagDetail(tag_id) {
	var data = new FormData();
	data.append("tag_id", tag_id);
	return post('/api/getTagDetail', data);
}

export function deleteTagToPost(params) {
	var data = new FormData();
	data.append("post_id", params.post_id);
	data.append("tag_id", params.tag_id);
	//console.log(params.post_id);
	//console.log(params.tag_id);
	return post('/api/deleteTagToPost', data);
}

export function addTagToPost(params) {
	var data = new FormData();
	data.append("post_id", params.post_id);
	data.append("tag_id", params.tag_id);
	console.log(params);
	
	return post('/api/addTagToPost', data);
}

export function createNotice(params) {
	var data = new FormData();
	data.append("username", params.username);
	data.append("title", params.title);
	data.append("content", params.content);
	console.log(params);
	return post('/api/createNotice', data);

}

export function allNotice() {
	return post('/api/allNotice', new FormData());
}

export function deleteNotice(notice_id) {
	var data = new FormData();
	data.append("notice_id", notice_id);
	return post('/api/deleteNotice', data);
}

export function myPosts(username) {
	var data = new FormData();
	data.append("username", username);
	return post('/api/myPosts', data);
}

export function getOrder(order_id) {
	var data = new FormData();
	data.append("order_id", order_id);
	return post('/api/getOrder', data);

}

export function myOrdersAsBuyer(username) {
	var data = new FormData();
	data.append("username", username);
	return post('/api/myOrdersAsBuyer', data);
}

export function myOrdersAsSaler(username) {
	var data = new FormData();
	data.append("username", username);
	return post('/api/myOrdersAsSaler', data);
}

export function getUserInfo(username) {
	var data = new FormData();
	data.append("username", username);
	return post('/api/getUserInfo', data);
}

export function getCommodityDetail(commodity_id) {
	var data = new FormData();
	data.append("commodity_id", commodity_id);
	return post('/api/getCommodityDetail', data);
}

export function cancelOrder(order_id) {
	var data = new FormData();
	console.log(order_id);
	data.append("order_id", order_id);
	return post('/api/cancelOrder', data);
}