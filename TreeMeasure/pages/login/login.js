// pages/login/login.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    identifier:'',
    password:'',
  },
  identifierInput:function(e){
    this.setData({
      identifier:e.detail.value
    })
  },
  passwordInput:function(e){
    this.setData({
      password:e.detail.value
    })
  },
  userLogin:function(){
    if(this.data.identifier=='')
    {
      wx.showToast({
        title: '用户名为空!请输入用户名!',
        icon: 'none',
        duration: 2000
      })
      return;
    }
    if(this.data.password=='')
    {
      wx.showToast({
        title: '密码为空!请输入密码!',
        icon: 'none',
        duration: 2000
      })
      return;
    }
    var that=this;
    wx.request({
      url: 'http://localhost:18081/userLogin',
        method:'GET',
        header:{'content-type':'application/x-www-form-urlencoded'},
        data:{
          'username': that.data.identifier,
          'password': that.data.password
       },
        success:function(res){
          if(res.data.code=="200")
          {
            wx.showToast({
              title: '登录成功',
              duration:2000
            })
            wx.navigateTo({
              url: '/pages/home_page/home_page?student_identifier='+that.data.identifier,
            })
          }
          else
          {
            wx.showToast({
              title: '用户名或密码错误!',
              icon: 'none',
              duration: 2000
            })
          }
        }
    })
  },
 
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})