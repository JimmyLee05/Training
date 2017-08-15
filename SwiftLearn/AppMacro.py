import UIKit

/* --------------------- appKey ------------------------ */

//JPush Key
let jpushKey 			= "0e025f950fbd63738d00866e"
//友盟key
let umengKey 			= "549278d2fd98c5d4770013f6"
//美洽key
let meiqiaAppKey 		= "53402fa92ca086ccd94e24919e1cdec3"
//微信appid
let wechatAppID 		= "wxd3ce3e59f1d014e"
//微信app secret
let wechatAppSercret 	= "72e4719b45f502a1ed2ad4899cf5767f"
//QQ appid
let qqAppID 			= "1104401219"
//QQ appKey
let qqAppSecret 		= "I4txMBKbHw9cK8Q2"
//Sina appid
let sinaAppID 			= "2922222176"
//Sina appKey 
let sinaAppSecret 		= "cf217476612b46b6c0180248fc14db37"
//facebook appid
let facebookAppID 		= "655074701317098"
//twitter appid
let twitterAppID 		= "dJzOku5AsB9EhDkud5nhWO46r"
//twitterAppSecret 
let twitterAppSecret 	= "hGwgNLbSW5y01dL7TePv7JCHfrQ3vRDbR6TXJLpSlTmh9maBwJ"

/* ---------------------- end ------------------------------ */

var isInJapan: Bool {
	return UIApplication.isoCountryCode?.lowercased() == "jp"
}

let japanServer 		= "info@fugu-innovation.com"

//购买小觅链接
var buyMyntURL: String {
	
	return String(format: "http://www.slightech.com/buy/mynt?ch=%@&lang=%@&region=%@", "ios", Locale.current.
		languageCode!, Locale.current.region)
}

//购买电池链接
var buyBatteryURL: String {
	return String(format: "http://www.slightech.com/buy/battery?ch=%@&lang=%@&region=%@", "ios", Locale.current.
		languageCode!, Locale.current.region)
}

/* ---------------------- 基础数据 ----------------------------- */

//窗体大小
let winRect 					= UIScreen.main.bounds
//窗体大小
let winSize 					= winRect.size
//缩放比例
let widthScale 					= winSize.width / 320
//高度比例
let heightScale 				= winSize.height / 667
//基准高度(iPhone6)
let baseWinHeight: CGFloat 		= 667
//状态栏高度
let statusBarHeight 			= UIApplication.shared.statusBarFrame.height
//navigationBar的背景色
let navigationBarColor 			= ColorStyle.kTunaColor
//展开背景色
let expandBackgroundColor 		= UIColor(hexString: "F2F2F2")
//segment背景色
let segmentBackgroundColors 	= [UIColor(hexString: "F8F8F8"), expandBackgroundColor]

/* ----------------------- end ----------------------------------- */

