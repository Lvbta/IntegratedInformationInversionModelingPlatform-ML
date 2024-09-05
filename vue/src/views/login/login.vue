<template>
  <div class="login">
    <div class="login-head">
    </div>
    <div class="login-content">
      <div class="content-welcome">
        <p>欢迎进入</p>
        <p>综合信息反演建模平台</p>
        <p>请在右侧登录>></p>
      </div>
      <div class="content-form">
        <div class="form">
          <div class="form-item">
            <label for="username">账号：</label>
            <input
              id="username"
              type="text"
              class="list-input"
              @blur="inputBulr('username')"
              v-model="user.username"
            />
            <div class="item-error-tip" ref="nameTip" v-show="nameTipBoolShow">
              账号不能为空
            </div>
          </div>
          <div class="form-item">
            <label for="paw">密码：</label>
            <input
              id="paw"
              type="password"
              @blur="inputBulr('password')"
              v-model="user.password"
            />
            <div class="item-error-tip" ref="pwdTip" v-show="pwdTipBoolShow">
              dwdwdw
            </div>
          </div>
          <div class="form-btn" @click="login">
            <button>登录</button>
          </div>
          <div class="form-bottom">
            <p>没有账号？请联系管理员</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "login",
  data () {
    return {
      user: {
        username: "admin",
        password: "123456",
      },
      pwdTipBoolShow: false,
      pwdTiphtml: "",
      nameTipBoolShow: false,
      nameTiphtml: "",
    };
  },
  methods: {
    inputBulr (name) {
      switch (name) {
        case "username":
          if (this.user.username === "") {
            this.nameTipBoolShow = true;
            this.nameTiphtml = "账号不能为空";
          } else {
            let regex = /^\w+@[0-9a-z]+\.[a-z]+$/;
            if (!regex.test(this.user.username)) {
              this.nameTipBoolShow = true;
              this.nameTiphtml = "输入正确邮箱地址";
            } else {
              this.nameTipBoolShow = false;
            }
          }
          break;
        case "password":
          if (this.user.password === "") {
            this.pwdTipBoolShow = true;
            this.pwdTiphtml = "密码不能为空";
          } else {
            var regex = new RegExp("(?=.*[0-9])(?=.*[a-zA-Z]).{8,18}"); //数字字母至少八个字符
            if (!regex.test(this.user.password)) {
              this.pwdTipBoolShow = true;
              this.pwdTiphtml = "无效密码";
            } else {
              this.pwdTipBoolShow = false;
            }
          }
          break;
      }
    },
    login () {
      this.inputBulr("username");
      this.inputBulr("password");
      if (
        this.user.username === "admin" &&
        this.user.password === "123456"
      ) {
        //alert("登录成功");
        this.$router.push("/working").catch(() => { });
      } else {
      }
    },
  },
};
</script>

<style scoped>
.login {
  height: 100%;
  background: url("../../assets/img/login-bg.png") no-repeat;
  background-size: 100% 100%;
}

.login-head {
  height: 180px;
  padding: 0 60px;
  margin-bottom: 50px;
}
.login-head .logo {
  float: left;
  position: relative;
  width: 50px;
  height: 50px;
  margin: 15px 0 0;
  background-size: 100% 100%;
}
.login-head .logo::after {
  position: absolute;
  content: "";
  width: 2px;
  height: 28px;
  right: -18px;
  top: 10px;
  background-color: #fff;
}
.login-head .title {
  float: left;
  padding-left: 36px;
  height: 60px;
  margin-top: 15px;
  line-height: 50px;
  font-size: 26px;
  font-weight: 600;
  color: #fff;
}
.login-content {
  width: 900px;
  height: 480px;
  overflow: hidden;
  margin: 0 auto;
  box-sizing: border-box;
}
.login-content .content-welcome {
  position: relative;
  float: left;
  width: 380px;
  height: 480px;
  padding: 60px 50px;
  background-color: rgba(22, 48, 76, 0.56);
  text-align: left;
  border-radius: 8px;
  box-sizing: border-box;
}
.login-content .content-welcome > :first-child {
  font-size: 38px;
  font-weight: 300;
  height: 100px;
  color: #2be1f1;
}
.login-content .content-welcome > :nth-child(2) {
  font-size: 24px;
  font-weight: 700;
  line-height: 60px;
  text-align: center;
  color: #2be1f1;
}
.login-content .content-welcome > :nth-child(3) {
  font-size: 16px;
  font-weight: 300;
  line-height: 60px;
  color: #2be1f1;
  bottom: 2px;
  position: absolute;
}
.content-form {
  position: relative;
  float: left;
  width: 500px;
  height: 480px;
  padding: 40px 50px;
  background-color: rgba(22, 48, 76, 0.56);
  text-align: left;
  border-radius: 8px;
  margin-left: 20px;
  box-sizing: border-box;
}
.form-item {
  margin-bottom: 30px;
}
.form-item label {
  display: block;
  font-size: 16px;
  height: 45px;
  font-weight: 400;
  color: #fff;
}
.form-item input {
  width: 100%;
  height: 43px;
  background-color: transparent;
  border: 1px solid #dcdcdc;
  border-radius: 6px;
  font-size: 12px;
  padding: 20px 20px;
  box-sizing: border-box;
  color: #fff;
}
.form-btn {
  margin-top: 50px;
  width: 100%;
  height: 45px;
  background-color: #2be1f1;
  border-radius: 6px;
  text-align: center;
  line-height: 45px;
}
.form-btn:hover {
  background-color: rgb(27, 182, 195);
  cursor: pointer;
}
.form-btn button {
  border: none;
  background-color: transparent;
}
.form-bottom p {
  position: absolute;
  bottom: 2px;
  font-size: 16px;
  font-weight: 300;
  line-height: 60px;
  color: #cecece;
}
.item-error-tip {
  position: absolute;
  color: #ed4014;
  font-size: 12px;
  line-height: 1;
  padding-top: 6px;
}
</style>