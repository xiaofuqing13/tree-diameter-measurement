// pages/home_page/home_page.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    src:"",
    tempFilePaths:'',
    filename:"",
    hiddenmodalput: true,
    params:"",
  },
uploadparams:function(){
  this.setData({
  	//注意到模态框的取消按钮也是绑定的这个函数，
  	//所以这里直接取反hiddenmodalput，也是没有毛病
    hiddenmodalput:!this.data.hiddenmodalput
  })
   
},
cancel: function () {
 
  this.setData({

    hiddenmodalput: true

  });

},
confirm: function () {
 
  this.setData({

    hiddenmodalput: true,

  })
  var that=this;
    wx.request({
        url: 'http://127.0.0.1:5000/uploadparams', //API地址
      　method: "POST",
        header:{'content-type':'application/x-www-form-urlencoded'},
        data:{
          'params': that.data.params
        },
        success: function (res) {
          console.log(res.data);  //控制台输出返回数据  
          
          wx.hideLoading()
          if(res.data=="100"){
            wx.showToast({
              title: '提交成功！',
              duration:2000
            })
          }
      }
    })
},
paramsInput:function(e){
  this.setData({
    params:e.detail.value
  })

},
pic: function (options) {
    var _this=this
    wx.chooseImage({
      count: 1, // 默认9
      sizeType: ['original', 'compressed'], // 可以指定是原图还是压缩图，默认二者都有
      sourceType: ['album', 'camera'], // 可以指定来源是相册还是相机，默认二者都有
      success: function (res) {
        // 返回选定照片的本地文件路径列表，tempFilePath可以作为img标签的src属性显示图片
        const tempFilePaths = res.tempFilePaths;
        wx.setStorageSync('tempFilePaths', tempFilePaths);
        _this.setData({
          src:res.tempFilePaths
        } )
        wx.showLoading({
          title: '上传中...',
      })
        var team_image = wx.getFileSystemManager().readFileSync(res.tempFilePaths[0], "base64")
        wx.request({
          url: 'http://127.0.0.1:5000/upload', //API地址
          　　　　　 　　　　　method: "POST",
          header: {　　'content-type': "application/x-www-form-urlencoded"},
          data: {image: team_image},//将数据传给后端
     
        success: function (res) {
            console.log(res.data);  //控制台输出返回数据  
            
            wx.hideLoading()
            if(res.data=="100"){
              wx.showToast({
                title: '上传成功！',
                duration:2000
              })
            }
        }
            })
      }
    })
  },
measure:function(){
  
    const that = this
    wx.showLoading({
          title: '测量中...',
          duration: 4000//持续的时间
      }),
      wx.request({
        url: 'http://127.0.0.1:5000/measure', //API地址
        　　　　　 　　　　　method: "GET",
        header: {　　'content-type': "application/x-www-form-urlencoded"},
        responseType:"arraybuffer",
        
      success: function (res) {
        console.log(res)
        const len=res.header.length
        const img=res.header.data
        let url ='data:image/png;base64,'+wx.arrayBufferToBase64(res.data)
        that.setData({
          codeUrl : url,     //设置data里面的图片url
          show:true
        })
      
        
        wx.showModal({
          title: '胸径大小（mm）', 
          confirmText: "确认",
          cancelText:"取消",
          content: res.header.length, 
          success: function(res) { 
            if (res.confirm) {//这里是点击了确定以后
              console.log('用户点击确定')
            } else {//这里是点击了取消以后
              console.log('用户点击取消')
            }
          }
          })
        },
        fail(res){
        Toast.clear();
        }
          })
},

/**
* 对话框取消按钮点击事件
*/
onCancel: function() {
  this.hideModal();
},
/**
* 对话框确认按钮点击事件
*/
onConfirm: function() {
  wx.showToast({
      title: '提交成功',
      icon: 'success',
      duration: 2000
  })
  this.hideModal();
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