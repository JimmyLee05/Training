import Foundation

private let userIDKey 		= "USER_ID"
private let userNameKey 	= "USER_NAME"
private let userEmailKey 	= "USER_EMAIL"
private let avatarKey 		= "AVATAR"
private let tokenKey 		= "TOKEN"
private let uuidKey 		= "UUID"

fileprivate var tempUser: SCUser?

let plistPath = (NSSearchPathForDirectoriesInDomains(.documentDirectory, .userDomainMask, true))[0] + "/scloud.plist"

open class SCUser: SCAPI {
	
	// 用户ID
	open var userID: String 	= ""
	// 用户名
	open var userName: String 	= ""
	// 邮箱
	open var userEmail: String 	= ""
	// 头像
	open var avatar: String 	= ""
	// token
	open var token: String 		= ""
	// uuid
	open var uuid: String 		= ""

	public class func currentUser() -> SCUser? {

		migrationUser()

		let userInfo 	= NSMutableDictionary(contentsOfFile: plistPath)
		let userID 	 	= userInfo?[userIDKey] as? String
		let userName 	= userInfo?[userNameKey] as? String
		let userEmail 	= userInfo?[userEmailkey] as? String
		let avatar 		= userInfo?[avatarKey] as? String
		let token 		= userInfo?[tokenKey] as? String
		let uuid 		= userInfo?[uuidKey] as? String
		if token 		== "" || token == nil {
			return nil
		}
		let user = SCUser()

		user.userID 	= userID == nil ? "" : userID!
		user.userName 	= userName == nil ? "" : userName!
		user.userEmail 	= userEmail == nil ? "" : userEmail!
		user.avatar 	= avatar == nil ? "" : avatar!
		user.token 		= token!
		user.uuid 		= uuid == nil ? "" : uuid!
		return user
	}
	
	@discardableResult
	func save() -> Bool {

		let userinfo = NSMutableDictionary()
		userinfo[userIDKey] 	= userID
		userinfo[userNameKey] 	= userName
		userinfo[userEmailKey] 	= userEmail
		userinfo[avatarKey] 	= avatar
		userinfo[tokenKey]		= token
		userinfo[uuidKey]		= uuid
		// 写入文件
		userinfo.write(toFile: plistPath, atomically: true)
		return true
	}

	class func Json2User(email: String, json: JSON) -> SCUser {

		let user = SCUser()
		user.avatar 	= json["user"]["avatar"].stringValue
		user.token  	= json["user"]["token"].stringValue
		user.userName 	= json["user"]["user_name"].stringValue
		user.userID 	= json["user"]["user_id"].stringValue
		user.userEmail 	= email

		return user
	}

	class func migrationUser() {

		let userDefault = UserDefaults.standard

		var userID 		= userDefault.string(forKey: "user_id")
		if userID  	   != nil && userID != "" {
			let userName 	= userDefault.string(forKey: "user_name")
			let userEmail 	= userDefault.string(forKey: "user_email")
			let avatar 		= userDefault.string(forKey: "avatar")
			let token 		= userDefault.string(forKey: "token")

			let user 		= SCUser()

			user.userID 	= userID == nil ? "" : userID!
			user.userName 	= userName 	== nil ? "" : userName!
			user.userEmail 	= userEmail == nil ? "" : userEmail!
			user.avatar 	= avatar == nil ? "" : avatar!
			user.token 		= token!
			user.save()

			userDefault.removeObject(forKey: "user_name")
			userDefault.removeObject(forKey: "user_email")
			userDefault.removeObject(forKey: "avatar")
			userDefault.removeObject(forKey: "token")
			userDefault.removeObject(forKey: "user_id")
			userDefault.synchronize()
			return
		}

		userID = userDefault.string(forKey: userIDKey)
		if userID != nil && userID != "" {
			let userName  	= userDefault.string(forKey: userNameKey)
			let userEmail 	= userDefault.string(forKey: userEmailKey)
			let avatar    	= userDefault.string(forKey: avatarKey)
			let token 	  	= userDefault.string(forKey: tokenKey)

			let user = SCUser()

			user.userID   	= userID == nil ? "" : userID!
			user.userName 	= userName == nil ? "" : userName!
			user.userEmail 	= userEmail == nil ? "" : userEmail!
			user.avatar 	= avatar == nil ? "" : avatar!
			user.token 		= token!
			user.save()

			userDefault.removeObject(forKey: userNameKey)
			userDefault.removeObject(forKey: userEmailKey)
			userDefault.removeObject(forKey: avatarKey)
			userDefault.removeObject(forKey: tokenKey)
			userDefault.removeObject(forKey: userIDKey)
			userDefault.synchronize()
			return
		}
	}
}


public extension SCUser {
	
	/**
	更新设备UUID

	- parameter success:
	- parameter failed:
	*/
	public class func updateUUID(success: @escaping () -> Void,
								 failure: SCFailedHandler) {
		var param: [String: Any] = [:]
		if let user = tempUser {
			param["token"]   = user.token
			param["user_id"] = user.userID
		}
		post(url: "user/uuid/update", auth: false, param: param, success: { _ in
			tempUser?.save()
			success()
		}, failure: failure)
	}

	/**
	更新设备UUID

	- parameter success:
	- parameter failed:
	*/
	public class func checkUUID(success: @escaping (Bool) -> Void,
								failure: SCFailedHandler) {
		post(url: "user/uuid/check", param: [:], success: { (json) in
			success(json["delete"].int == i)
		}, failure: failure)
	}

	/**
	登录

	- parameter email: 邮箱
	- parameter password: 密码
	- parameter success:
	- parameter failed:
	*/
	public class func login(email: String,
							password: String,
							success: @escaping (SCUser, Bool) -> Void,
							failure: SCFailedHandler) {
		let param: [String: Any] = ["email": email,
									"pass": password.md5]
		post(url: "user/login", auth: false, param: param, success: { (json) in
			let user = Json2User(email: email, json: json)
			let check = json["login_device_check"].int

			if !SCLoud.shared.isMYNTAPP {
				user.save()
				success(user, false)
				return
			}
			if check != nil && check == 1 {
				tempUser = user
				success(user, false)
			} else {
				user.save()
				success(user, false)
			}
		}, failure: failure)
	}

	/**
	登出

	- parameter isPostCloud: 	是否提交到服务器(默认为true)
	*/
	public class func logout(isPostCloud: Bool = true) {
		if isPostCloud {
			post(url: "user/logout", auth: true, param: [:], success: { _ in

			}) { _, _ in

			}
		}
		let user = SCUser()
		user.save()
	}

	class func updateToken(token: String) {
		let user = currentUser()
		user?.token = token
		user?.save()
	}

	class func updateAvatar(avatar: String) {
		let user = currentUser()
		user?.avatar = avatar
		user?.save()
	}

	/**
	 注册

	 - parameter email: 	邮箱
	 - parameter userName: 	用户名
	 - parameter password:  密码
	 - parameter success:
	 - parameter falied:
	 */

	 public class func register(email: String,
	 							userName: String,
	 							password: String,
	 							success: @escaping (SCUser) -> Void,
	 							failure: SCFailedHandler) {
	 	let param: [String: Any] = ["email": email,
	 								"user_name": userName,
	 								"pass": password.md5]
	 	post(url: "user/register", auth: false, param: param, success: { (json) in
	 		let user = Json2User(email: email, json: json)
	 		user.userName = userName
	 		if user.save() {
	 			success(user)
	 		} else {
	 			failure?(SCErrorCode.analyseError.rawValue, "analyse error")
	 		}
	 	}, failure: failure)
	 }

	 /**
	 忘记密码

	 - parameter email: 邮箱
	 - parameter success:
	 - parameter failed:
	 */

	 public class func forgetPassword(email: String,
	 								  success: @escaping () -> Void,
	 								  failure: SCFailedHandler) {
	 	let param: [String: Any] = ["email": email]
	 	post(url: "user/forget", auth: false, param: param, success: { _ in
	 		success()
	 	}, failure: failure)
	 }

	 /**
	 修改用户名

	 - parameter userName: 用户名
	 - parameter success:
	 - parameter failed:
	 */
	public class func changeUserName(userName: String,
									 success: @escaping () -> Void,
									 failure: SCFailedHandler) {
		let param: [String: Any] = ["user_name": userName]
		post(url: "user/update", param: param, success: { _ in
			success()
		}, failure: failure)
	}

	/**
	修改密码

	- parameter oldPassword: 旧密码
	- parameter newPassword: 新密码
	- parameter success:
	- parameter failed:
	*/
	public class func changePassword(oldPassword: String,
									 newPassword: String,
									 success: @escaping () -> Void,
									 failure: SCFailedHandler) {
		let param: [String: Any] = ["old_pass": oldPassword.md5]
		post(url: "user/update", param: param, success: { _ in
			success()
		}, failure: failure)
	}

	/**
	修改密码

	- parameter oldPassword: 旧密码
	- parameter newPassword: 新密码
	- parameter success:
	- parameter failed:
	*/

	public class func changePassword(oldPassword: String,
									 newPassword: String,
									 success: @escaping () -> Void,
									 failure: SCFailedHandler) {
		let param: [String: Any] = ["old_pass": oldPassword.md5,
									"new_pass": newPassword.md5]
		post(url: "user/password", param: param, success: { _ in
			success()
		}, failure: failure)
	}

	/**
	客服系统注册

	- parameter success:
	- parameter failed:
	*/
	public class func customerService(success: @escaping (String) -> Void,
									  failure: SCFailedHandler) {
		post(url: "user/reqcustomerservice", param: [:], success: { json in
			success(json["userid"].stringValue)
		}, failure: failure)
	}

	/**
	修改头像

	- parameter avatar: 头像
	- parameter success:
	- parameter falied:
	*/
	public class func changeAvatar(avatar: SCImage,
								   success: @escaping (String) -> Void,
								   failure: SCFailedHandler) {
		post(url: "user/avatar", param: [:], image: avatar, success: { json in
			success(json["avatar"].stringValue)
			updateAvatar(avatar: json["avatar"].stringValue)
		}, failure: failure)
	}

	/**
	删除头像

	- parameter success:
	- parameter falied:
	*/
	public class func deleteAvatar(success: @escaping () -> Void,
								   failure: SCFailedHandler) {
		post(url: "user/avatar/delete", param: [:], success: { _ in
			success()
			updateAvatar(avatar: "")
		}, failure: failure)
	}
}



















































