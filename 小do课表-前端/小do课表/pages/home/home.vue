<template>
	<view class="contain-box">
		<view class="show-info">
			<view class="show-title">
				<text class="name-text">{{ user }}</text>
				同学,你好！
			</view>
			<view class="small-title">
				欢迎使用小杜课表（武理专属）
			</view>
		</view>
		<view class="bottom-list">
			<view class="show-buttons">
				<view class="box-show-item">
					<view class="infos"><image mode="widthFix" src="../../static/icon/username.png"></image></view>
					<input type="number" v-model="username" placeholder="请输入学号" maxlength="13" />
					<image class="icon" src="../../static/icon/del.png" mode="widthFix" @click="reset"></image>
				</view>
				<view class="box-show-item">
					<view class="infos"><image mode="widthFix" src="../../static/icon/password.png"></image></view>
					<input v-model="password" placeholder="请输入密码" :password="!isShow" />
					<image class="icon" mode="widthFix" src="../../static/icon/hide.png" v-show="!isShow" @click="changeShow"></image>
					<image class="icon" mode="widthFix" src="../../static/icon/hide_active.png" v-show="isShow" @click="changeShow"></image>
				</view>
			</view>
			<view class="submit-button">
				<button type="primary" @click="save2storage">登录</button>
				<button type="primary" @click="reset">重置</button>
			</view>
			
		</view>
	</view>
</template>

<script>
export default {
	data() {
		return {
			user:'',
			username: '',
			password: '',
			isShow: false
		};
	},
	methods: {
		save2storage() {
			// console.log(this.username, this.password);
			if(this.username=='' || this.password==''){
				uni.showToast({
					title: '要输入完整的信息才能使用哦！',
					icon: 'none'
				});
				return;
			}
			
			new Promise(async reslove => {
				let res = await uni.request({
					// url: `http://127.0.0.1:5666/getUser?username=${this.username}&password=${this.password}`
					url: `http://duing.site:5666/getUser?username=${this.username}&password=${this.password}`
				});
				// console.log('+++++++++++++',res)
				if(res[1].data.user.name == undefined || res[1].data.user.name == null || res[1].data.user.name == ''){
					uni.showLoading({
						title: '登录中...'
					});
					setTimeout(() => {
						uni.showToast({
							title: '学号或密码错误！请重新输入',
							icon: 'none'
						});
					}, 1000);
				}else{
					this.user = res[1].data.user.name;
					uni.setStorageSync('user', this.user);
					
					uni.showLoading({
						title: '保存中...'
					});
					uni.setStorageSync('username', this.username);
					uni.setStorageSync('password', this.password);
					
					uni.hideLoading();
					uni.showToast({
						title: '登录成功！',
						icon: 'none'
					});
					setTimeout(() => {
						uni.switchTab({
							url: '/pages/index/index'
						});
					}, 1000);
				}
			});
		},
		reset() {
			uni.showModal({
				title: '您确定要注销吗？',
				content: '注销后需要重新绑定账号哦!',
				success: res => {
					if (res.confirm) {
						uni.clearStorageSync();
						this.username = '';
						this.password = '';
					}
				}
			});
		},
		changeShow() {
			this.isShow = !this.isShow;
		}
	},
	onReady() {
		let username = uni.getStorageSync('username');
		let password = uni.getStorageSync('password');
		let user = uni.getStorageSync('user');
		this.username = username;
		this.password = password;
		this.user = user;
	}
};
</script>

<style scoped>
/* 总体 */
.contain-box {
	width: 100%;
	height: 100vh;
	display: flex;
	flex-direction: column;
	background-color: #D4F2E7;
}
/* 图片 */
.back-pic {
	width: 100%;
}
.back-pic image {
	width: 100%;
	animation: linear yaobai 1s;
}
@keyframes uptotop {
	from {
		transform: translateY(200rpx);
		opacity: 0;
	}
	to {
		transform: translateY(0rpx);
		opacity: 1;
	}
}
@keyframes rot {
	from {
		transform: scale(0.5);
	}
	to {
		transform: scale(1);
	}
}
@keyframes yaobai {
	0% {
		transform: rotate(25deg);
	}
	25% {
		transform: rotate(-12deg);
	}
	50% {
		transform: rotate(0deg);
	}
	75% {
		transform: rotate(12deg);
	}
	100% {
		transform: rotate(0);
	}
}
/* 底部整体 */
.bottom-list {
	margin-top: 200rpx;
	width: auto;
	background-color: #f5f5f5;
	border-radius: 30rpx 30rpx 0 0;
	position: relative;
	padding: 30rpx;
	top: -80rpx;
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
	animation: linear uptotop 1s;
}

/* 显示info栏目 */
.show-info {
	background-color: #FFE4E1;
	align-items: center;
	border-radius: 20rpx;
	box-shadow: 0rpx 10rpx 5rpx #808080;
	display: flex;
	flex-direction: column;
	text-align: left;
	margin-top: 20rpx;
	padding: 15rpx;
	animation: linear rot 1s;
}
.show-title {
	font-size: 40rpx;
	font-weight: 700;
	color: #00FF7F;
	margin-top: 20rpx;
	margin-bottom: 20rpx;
}
.name-text{
	color: #00BFFF;
	margin-right: 30rpx;
}
.small-title {
	font-size: 30rpx;
	color: #808080;
}
/* 输入框处理 */
.show-buttons {
	margin-top: 50rpx;
	background-color: #F0FFF0;
	padding: 18rpx;
	display: flex;
	flex-direction: column;
	width: 70%;
	border-radius: 18px;
}
.box-show-item {
	display: flex;
	flex-direction: row;
	width: 100%;
	align-items: center;
}
.box-show-item image {
	width: 60rpx;
	height: 60rpx;
	margin: 5rpx;
}
.box-show-item input {
	/* width: calc(100%-130rpx); */
}
/* buttons */
.submit-button {
	display: flex;
	flex-direction: row;
	margin-top: 30rpx;
}
.submit-button > * {
	flex: 1;
	margin: 50rpx;
	background-color: #00FFFF;
}
</style>
