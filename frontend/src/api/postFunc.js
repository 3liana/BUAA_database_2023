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