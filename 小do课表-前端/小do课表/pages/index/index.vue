<template>
	<view class="index-container">
		<view class="kebiao-container">
			<!-- 表头 -->
			<view class="kebiao-title">
				<view class="kong"></view>
				<view class="date-list">
					<view class="date-list-item" v-for="(item, index) in showDate" :class="{ current: today == item.date }" :key="item.date">
						<view class="week">{{ item.week }}</view>
						<view class="date">{{ item.date }}</view>
					</view>
				</view>
			</view>
			
			<view class="lesson-container">
				<view class="left">
					<view v-for="(item, index) in [1,2,3,4,5,6,7,8,9,10,11,12,13]" class='left-item'>{{item}}</view>
				</view>
				
				<view class="kebiao-body">
					<!-- 表身 -->
					<view class="biao-right">
						<view
							class="title-list-item"
							:class="['where' + index, { 'len-three': item.len === 3 }, { isOpacity: !item.show }]"
							v-for="(item, index) in lessonlist"
							:key="item.count"
							@click="showDetail(item)"
						>
							<view class="lesson">{{ item.lesson_name }}</view>
							<view class="where">{{ item.place }}</view>
						</view>
					</view>
				</view>
				
			</view>
			
		</view>
		<!-- <view class="choose-week">
			<button type="primary" @click="buttonControl(1)">上一周</button>
			<button type="primary" @click="buttonControl(2)">回当前周</button>
			<button type="primary" @click="buttonControl(3)">下一周</button>
		</view> -->
		<view class="show-message-detail" v-if="clicked" @click="exitDetail">
			<view class="focus">
				<view class="name">{{ currentClick.lesson_name }}</view>
				<view class="place">{{ currentClick.place }}</view>
				<view class="time">{{ currentClick.time_desc }}</view>
				<view class="timeweek">{{ currentClick.week_desc }}</view>
			</view>
		</view>
		<view class="change-week-menu" v-show="navbarclick">
			<view class="box">
				<view :class="[index!=todayWeek?'menu-item':'menu-item-current']" v-for="(item, index) in 20" @click="changeWeek(index)" :key="item">
					<text v-if="index == currentWeek">>></text>
					<text>第{{ item }}周</text>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
export default {
	data() {
		return {
			// 存储日期
			showDate: null,
			// 存储课程
			lessonlist: null,
			// 存储当前周
			currentWeek: 0,
			// 起始日
			// startDate:[2020,8,7],
			startDate: [],
			// 存储请求的原始数据
			rawData: null,
			// 今天的日期
			today: null,
			// 今天的星期
			week: null,
			// 记录当前周
			todayWeek: null,
			// 点击的
			currentClick: null,
			// 点击控制
			clicked: false,
			//navbarclick
			navbarclick: false
		};
	},
	methods: {
		// 修改周
		buttonControl(choose) {
			switch (choose) {
				case 1: {
					if (this.currentWeek > 0) {
						this.changeWeek(this.currentWeek - 1);
					} else {
						uni.showToast({
							title: '没有上一个了喔',
							icon: 'none'
						});
					}
					break;
				}
				case 2: {
					this.changeWeek(this.todayWeek);
					break;
				}

				case 3: {
					if (this.currentWeek < 19) {
						this.changeWeek(this.currentWeek + 1);
					} else {
						uni.showToast({
							title: '没有下一个了喔',
							icon: 'none'
						});
					}
					break;
				}
			}
		},
		// 修改课表
		async changeWeek(index) {
			uni.showLoading({
				title: '加载中'
			});
			this.navbarclick = false;
			this.currentWeek = index;
			await this.refresh();
			uni.setNavigationBarTitle({
				title:`本周是第${this.currentWeek+1}周`
			})
			uni.hideLoading();
		},

		// 点击了详情
		showDetail(item) {
			if (!item.show) {
				return;
			} else {
				this.currentClick = item;
				this.clicked = true;
			}
		},
		// 退出显示
		exitDetail() {
			this.clicked = false;
		},
		getDate(count) {
			// count:周数
			// 获取到学期开始的第一天
			let firstDay = new Date(this.startDate[0], this.startDate[1], this.startDate[2]);
			// 获取到当前周的第一天
			let currentDay = new Date(firstDay.setTime(firstDay.getTime() + 7 * count * 86400000));
			let response = [];
			// 返回要求的周数的未来七天
			for (let i = 0; i < 7; i++) {
				response.push(new Date(currentDay.setTime(currentDay.getTime()) + i * 1000 * 60 * 60 * 24));
			}
			return response;
		},
		updateParse() {
			let weekdays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
			this.week = weekdays[new Date().getDay()];

			const { parse, datelist } = this.parseData(this.rawData, this.currentWeek);
			this.lessonlist = parse;
			this.showDate = datelist.map(item => {
				return {
					date: item.getMonth() + 1 + '-' + item.getDate(),
					week: weekdays[item.getDay()]
				};
			});
		},
		parseData(data, count) {
			let j = 0;
			let parse = [];
			let datelist = this.getDate(count);
			for (let i = 1; i <= 35; i++) {
				// 用来标记是否这里有课，没有就填充一个
				let flag = false;
				// 判断是否位置匹配
				while (j < data.length && data[j].count === i) {
					// 处理同序号
					// 判断匹配的这个数据是否属于本周
					let week = count + 1;
					let currentItemWeek = data[j].week_num.split('-');
					currentItemWeek = currentItemWeek.map(item => Number.parseInt(item));
					// 如果当前位置符合本周
					if (week >= currentItemWeek[0] && week <= currentItemWeek[1]) {
						// 加入datelist且两边同时后移
						// 计算节次
						let countNum = data[j].time_num.split('-');
						countNum = countNum[1] - countNum[0] + 1;
						parse.push({
							show: true,
							len: countNum,
							count: i,
							place: data[j].place,
							week_desc: data[j].week_desc,
							lesson_name: data[j].lesson_name,
							time_desc: '第' + data[j].time_desc
						});
						// 退出循环，位置往后挪
						flag = true;
						while (j < data.length && data[j].count === i) {
							// 跳到下一个位置
							j++;
						}
						break;
					} else {
						// 不符合位置，那么单独把j后移一位,继续进行循环
						j++;
					}
				}
				// 当前位置没找到有课，插入一个空的
				if (!flag) {
					parse.push({
						show: false,
						len: 2,
						count: i,
						place: '',
						week_desc: '',
						lesson_name: '',
						time_desc: ''
					});
				}
			}
			//console.log(parse)
			return {
				datelist,
				parse
			};
		},
		async refresh() {
			return new Promise(async reslove => {
				let username = uni.getStorageSync('username');
				let password = uni.getStorageSync('password');
				if (username != '' && password != '') {
					// 不为空就去请求数据
					// 读取缓存，有缓存直接用缓存
					let data = uni.getStorageSync('rawData');
					if (!data) {
						// 没缓存就去取
						let res = await uni.request({
							// url: `http://127.0.0.1:5666/getTables?username=${username}&password=${password}`
							url: `http://duing.site:5666/getTables?username=${username}&password=${password}`
						});
						res = res[1];
						data = res.data.data;
						// console.log(data);
						uni.setStorageSync('rawData', data);
					}

					// console.log(data);
					// 存储它
					this.rawData = data;
					// 解析数据
					// count就是第几周
					// this.currentWeek
					this.updateParse();

					// console.log(this.lessonlist, this.showDate);
					reslove('ok');
				} else {
					uni.showToast({
						icon: 'none',
						title: '您还没有登录哦！'
					});
					reslove('no');
				}
			});
		},
		async refreshByAPI() {
			return new Promise(async reslove => {
				let username = uni.getStorageSync('username');
				let password = uni.getStorageSync('password');
				if (username != '' && password != '') {
					// 不为空就去请求数据
					// 读取缓存，有缓存直接用缓存
					let res = await uni.request({
						// url: `http://127.0.0.1:5666/getTables?username=${username}&password=${password}`
						url: `http://duing.site:5666/getTables?username=${username}&password=${password}`
					});

					res = res[1];
					let data = res.data.data;
					//console.log(data);
					if (res.data.data.length == 0) {
						uni.showToast({
							title: '学号或密码错误！请重新登录',
							icon: 'none'
						});
						setTimeout(() => {
							uni.switchTab({
								url: '/pages/home/home'
							});
						}, 1000);
						return;
					}
					
					uni.setStorageSync('rawData', data);
					this.rawData = data;
					this.updateParse();
					reslove();
				} else {
					uni.showToast({
						icon: 'none',
						title: '您还没有登录哦！'
					});
					reslove();
				}
			});
		}
	},
	async onPullDownRefresh() {
		// console.log('test');
		await this.refreshByAPI();
		uni.stopPullDownRefresh();
	},
	async onLoad() {
		let today = new Date();
		this.startDate = uni.getStorageInfoSync('startDate');
		if (!startDay) {
			this.startDate = [2020, 8, 7];
			let test = await uni.request({
				// url: 'http://127.0.0.1:5666/getInfo'
				url: 'http://duing.site:5666/getInfo'
			});
			// console.log(test);
			if (!test[1].data.data.start_date) {
				uni.showToast({
					title: '网络出错！',
					icon: 'none'
				});
				return;
			}
			this.startDate = test[1].data.data.start_date;
			uni.setStorageSync('startDate', this.startDate);
		}
		let startDay = new Date(this.startDate[0], this.startDate[1], this.startDate[2]);
		let test = (today.getTime() - startDay.getTime()) / (7 * 86400 * 1000) + '';
		// 截断
		let week = Number.parseInt(test.substring(0, test.indexOf('.')));

		this.today = today.getMonth() + 1 + '-' + today.getDate();

		if (week > 19) {
			week = 19;
		}
		if (week < 0) {
			week = 0;
		}
		this.todayWeek = week;
		this.currentWeek = week;
		//console.log(week);
		let ok = await this.refresh();
		if (ok === 'no') {
			setTimeout(() => {
				uni.switchTab({
					url: '/pages/home/home'
				});
			}, 500);
		}
		if(ok=='ok'){
			uni.setNavigationBarTitle({
				title:`本周是第${this.todayWeek+1}周`
			})
		}
	},
	onNavigationBarButtonTap() {
		// console.log('clicked');
		this.navbarclick = !this.navbarclick;
	}
};
</script>

<style scoped>
.left{
	margin-top: 100rpx;
}
.left-item{
	width: 30rpx;
	height: 125rpx;
	font-size: 9pt;
	justify-content: center;
	display: flex;
	align-items: center;
	background-color: #00BFFF;
}	
.lesson-container{
	display: flex;
}

.index-container {
	display: flex;
	flex-direction: column;
	width: 100%;
}
.kebiao-title {
	display: flex;
	flex-direction: row;
	width: 95.5%;
	padding: 1%;
	position: fixed;
	background-color: #FFFACD;
	margin-left: 32rpx;
}
.date-list {
	width: calc(100%-180rpx);
	display: flex;
	flex-direction: row;
	justify-content: center;
	align-items: center;
	text-align: center;
}
.date-list-item {
	display: flex;
	flex-direction: row;
	flex-wrap: wrap;
	width: 14.8%;
	font-size: 35rpx;
	margin: 0rpx 18rpx;
	flex: 1;
}
.date {
	font-size: 15rpx;
}
/* 表身 */
.kebiao-body {
	display: flex;
	margin-top: 100rpx;
	margin-left: 17rpx;
	width: 100%;
	padding: 1%;
}
/* 表格 */
.biao-right {
	display: flex;
	flex-direction: row;
	flex-wrap: wrap;
}
.title-list-item {
	/*==========注意============*/
	width: 13%;
	font-size: 30rpx;
	text-align: center;
	color: #ffffff;
	padding: 3rpx;
	margin: 2rpx;
	height: 250rpx;
	border-radius: 15rpx;
	/* border: 1px solid; */
	/* animation: 1s goaway linear; */
}
@keyframes opacity2show {
	from {
		opacity: 0;
	}
	to {
		opacity: 1;
	}
}
@keyframes goaway{
	from{

	}
	to{

	}
}
.lesson {
	width: 100%;
	overflow: hidden;
	text-overflow: ellipsis;
	display: -webkit-box;
	-webkit-line-clamp: 2;
	-webkit-box-orient: vertical;
}
.where {
	overflow: scroll;
	/* text-overflow: ellipsis; */
	width: 100%;
}
.isOpacity {
	opacity: 0;
}
.len-three {
	padding-bottom: 50rpx;
}

/*  */
.show-message-detail {
	position: fixed;
	left: 0;
	right: 0;
	top: 0;
	bottom: 0;
	background-color: rgba(0, 0, 0, 0.5);
	color: white;
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
	text-align: center;
	animation: 0.3s opacity2show linear;
}
.focus {
	width: 600rpx;
	height: 320rpx;
	font-size: 60rpx;
	border-radius: 30rpx;
	background-color: #DAA520;
	background-position: center;
	background-size: 100%;
}
/* 周数控制 */
/* .choose-week {
	display: flex;
	flex-direction: row;
} */
/* change-week-menu */
.change-week-menu {
	position: fixed;
	top: 0;
	right: 0rpx;
	left: 0;
	bottom: 0;
	margin-top: 45px;
}
.box {
	float: right;
	background-color: #f5f5f5;
	overflow: scroll;
	height: 400rpx;
	width: 300rpx;
	text-align: center;
	font-size: 40rpx;
	color: #FF00FF;
	background-color: #FFE4B5;
	border-radius: 15rpx 0 0 15rpx;
}
.current {
	background-color: #00FA9A;
	border-radius: 10rpx;
	color: white;
	text-align: center;
	justify-content: center;
}
.menu-item {
	margin: 8rpx;
	border-top: #ffffff 1rpx solid;
}
.menu-item-current {
	margin: 8rpx;
	border-top: #ffffff 1rpx solid;
	color: #007AFF;
}

.where0 {
	background-color: #00CED1;
}
.where7 {
	background-color: #00CED1;
	margin-bottom: 20px;
}
.where14 {
	background-color: #00CED1;
}
.where21 {
	background-color: #00CED1;
}
.where28 {
	background-color: #00CED1;
}

.where1 {
	background-color: #fd79a8;
}
.where8 {
	background-color: #fd79a8;
	margin-bottom: 20px;
}
.where15 {
	background-color: #fd79a8;
}
.where22 {
	background-color: #fd79a8;
}
.where29 {
	background-color: #fd79a8;
}

.where2 {
	background-color: #FFA500;
}
.where9 {
	background-color: #FFA500;
	margin-bottom: 20px;
}
.where16 {
	background-color: #FFA500;
}
.where23 {
	background-color: #FFA500;
}
.where30 {
	background-color: #FFA500;
}

.where3 {
	background-color: #8A2BE2;
}
.where10 {
	background-color: #8A2BE2;
	margin-bottom: 20px;
}
.where17 {
	background-color: #8A2BE2;
}
.where24 {
	background-color: #8A2BE2;
}
.where31 {
	background-color: #8A2BE2;
}

.where4 {
	background-color: #00FF00;
}
.where11 {
	background-color: #00FF00;
	margin-bottom: 20px;
}
.where18 {
	background-color: #00FF00;
}
.where25 {
	background-color: #00FF00;
}
.where32 {
	background-color: #00FF00;
}

.where5 {
	background-color: #FF00FF;
}
.where12 {
	background-color: #FF00FF;
	margin-bottom: 20px;
}
.where19 {
	background-color: #FF00FF;
}
.where26 {
	background-color: #FF00FF;
}
.where33 {
	background-color: #FF00FF;
}

.where6 {
	background-color: #ffaec8;
}
.where13 {
	background-color: #ffaec8;
	margin-bottom: 20px;
}
.where20 {
	background-color: #ffaec8;
}
.where27 {
	background-color: #ffaec8;
}
.where34 {
	background-color: #ffaec8;
}
</style>
