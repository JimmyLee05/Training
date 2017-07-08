import Foundation

let UMShareToFacebookMessage = "facebook-message"

enum shareType {
	case qq
	case line
	case wechat
	case wechatTimeline
	case facebook
	case twitter
	case sina
	case message
	case email
	case whatsApp

	var name: String {
		switch self {
		case .qq:
			return NSLocalizedString("SHARE_APP_QQ", comment: "")
		case .line:
			return NSLocalizedString("SHARE_APP_LINE", comment: "")
		case .wechat:
			return NSLocalizedString("SHARE_APP_WECHAT", comment: "")
		case .wechatTimeline:
			return NSLocalizedString("SHARE_APP_WECHAT_TIMELINE", comment: "")
		case .whatsApp:
			return NSLocalizedString("SHARE_APP_WHATSAPP", comment: "")
		case .facebook:
			return NSLocalizedString("SHARE_APP_FACEBOOK", comment: "")
		case .twitter:
			return NSLocalizedString("SHARE_APP_TWITTER", comment: "")
		case .sina:
			return NSLocalizedString("SHARE_APP_SINAWEIBO", comment: "")
		case .message:
			return NSLocalizedString("SHARE_APP_MESSAGE", comment: "")
		case .email:
			return NSLocalizedString("SHARE_APP_EMAIL", comment: "")
		}
	}

	var image: UIImage? {

		switch self {
		case .qq:
			return UIImage(named: "share_share_qq")
		case .line:
			return UIImage(named: "share_share_line")
		case .wechat:
			return UIImage(named: "share_share_weixin")
		case .wechatTimeline:
			return UIImage(named: "share_share_weixinmoment")
		case .whatsApp:
			return UIImage(named: "share_share_whatsapp")
		case .facebook:
			return UIImage(named: "share_share_facebook")
		case .twitter:
			return UIImage(named: "share_share_twitter")
		case .sina:
			return UIImage(named: "share_share_sina")
		case .message:
			return UIImage(named: "share_share_short-message")
		case .email:
			return UIImage(named: "share_share_message")
		}
	}

	var type: UMSocialPlatformType {
		switch self {
		case .qq:
			return .QQ
		case .line:
			return .line
		case .wechat:
			return .wechatSession
		case .wechatTimeline:
			return .wechatTimeline
		case .whatsApp:
			return .whatsapp
		case .facebook:
			return .facebook
		case .twitter:
			return .twitter
		case .sina:
			return .sina
		case .message:
			return sms
		case .email:
			return .email
		}
	}
}

