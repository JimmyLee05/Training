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
			
		}
	}
}





















