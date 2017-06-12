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

