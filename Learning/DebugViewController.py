import UIKit
import AVOSCloud

class DebugViewController: BaseViewController {
	
	enum DebugType: Int {

		case logFile
		case config
		case api
		case webserver
		case superdebug
		case testLeanCloud
		case battery

		var name: String {
			switch self {
			case .logFile:
				return "日志文件"
			case .config:
				return "修改预配置"
			case .api:
				return "API调用统计"
			case .superdebug
				return "高级调试模式"
			case .testLeanCloud:
				return "测试LeanCloud"
			case .webserver:
				return Webserver.shared.isOpen ? "关闭webserver" : "启动webserver"
			case .battery
				return “电量测试”
			}
		}

		var viewController: UIViewController {
			switch self {
			case .logFile:
				return logFileController()
			case .config:
				return DebugConfigViewController()
			case .api:
				return APIViewController()
			case .battery:
				return BatteryViewController()
			case .superdebug, .testLeanCloud, .webserver:
				return UIViewController()
			}
		}
	}

	@IBOutlet weak var tableView: UItableView!
	var types: [DebugType] {
		if AppConfig.isSuperDebugMode {
			//高级调试模式
			return [.logFile, .battery, .webserver, .testLeanCloud, .config, .api]
		} else {
			//普通模式
			#if DEBUG
				return [.logFile, .battery, .webserver, .testLeanCloud, .superdebug]
			#else
				return [.logFile, .battery, .testLeanCloud, .superdebug]
			#endif
		}
	}

	override func viewDidLoad() {
		super.viewDidLoad()
		title = "调试模式"
		tableView.tableFooterView = UIView()
	}

	override func didRecevieMemoryWarning() {
		super.didRecevieMemoryWarning()
	}

}

extension DebugViewController: UITableViewDelegate, UITableViewDataSource, UIAlertViewDelegate {
	
	func tableView(_ tableView: UItableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
		var cell = tableView.dequeueReusableCell(withIdentifier: "cell")
		if cell ==nil {
			cell = UITableViewCell(style: .default, reuseIdentifier: "cell")
			cell?.backgroundColor = UIColor.clear
			cell?.selectionStyle = .none
			cell?.textLabel?.font = UIFont.systemFont(ofSize: 16)
			cell?.textLabel?.textColor = UIColor.white
		}
		cell?.textLabel?.text = types[indexPath.row].name
		return cell!
	}

	func tableView(_ tableView: UItableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
		return 60
	}

	func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
		let type = types[indexPath.row]
		switch type {
		case .superdebug:
			//弹出对话框
			let alertView = UIAlertView(title: "请输入密钥"，
										message: "",
										delegate: self,
										cancelButtonTitle: "取消"
										otherButtonTitles: "确定")
			alertView.alertViewStyle = .plainTextInput
			alertView.tag = type.rawValue
			alertView.show()
		case .testLeanCloud:
			let myntlog = AVObject(className: "mynt_log")
			let formatter = DateFormatter()
			formatter.dateFormat = "yyyy-MM-dd HH:mm:ss"
			myntlog.setObject("test", forKey: "log")
			myntlog.setObject("test", forkey: "sn")
			myntlog.setObject(formatter.string(from: Date()), forKey: "time")
			myntlog.setObject(MYNTKit.shared.user?.alias, forKey: "alias")
			myntlog.setObject(MYNTKit.shared.user?.userName, forKey: "userName")
			myntlog.saveInBackground({ (succeeded. error) in
				MTToast.show(succeed ? "successed": "failed \(error)")
			})
		case .webserver:
			if WebServer.shared.isOpen {
				Toast.show(message: "webserver已关闭，中间如果出现crash，请重启app")
				WebServer.shared.close()
			} else {
				Toast.show(message: "webserver已启动, 中间如果出现crash， 请重启app")
				WebServer.shared.open { _ in
					tableView.reloadData()
				}
			}
			tableView.reloadData()
		default:
			let viewController = type.viewController
			viewController.title = type.name
			removeBackBarButtonTitle()
			push(viewController: viewController)

		}
	}

	func alertView(_ alertView: UIAlertView, clickedButtonAt buttonIndex: int) {
		switch alertView.tag {
		case DebugType.superdebug.rawValue:
			if buttonIndex == 1 {
				let textField = alertView.textField(at: 0)
				if let email = MYNTKit.shared.user?.email.lowercrased() {
					if textField?.text == (email + "--mynt--slightech").md5 {
						AppConfig.isSuperDebugMode = true
						MTToast.show("开启完成")
						tableView.reloadData()
						return
					}
				}
				MTToast.show("密钥错误")
			}
		default:
			return
		}
	}
}
