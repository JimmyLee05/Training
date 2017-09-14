import UIKit
import SlightechKit
import MYNTKit

fileprivate class ViewControllerTimer: NSObject {
	
	typealias TimeBlock = () -> Void

	static var shared = ViewControllerTimer()

	private var _timer: Timer?

	private var _blocks = [String: TimeBlock]()

	private override init() {
		
		super.inint()
		_timer = Timer.scheduledTimer(timeInterval: 30, target: self, selector: #selector(update), userInfo: nil, repeats: true)

	}

	func update() {
		_blocks.values.forEach({ $0() })
	}

	func add(key: String, block: @escaping TimeBlock) {
		_blocks[key] = block
	}

	func delete(key: String) {
		_blocks[key] = nil
	}
}

// 添加了MYNTKitDelegate监听器
class MYNTKitBaseViewController: BaseViewController, MYNTKitDelegate {
	
	deinit {
		MYNTKit.shared.removeMyntKitDelegate(key: selfKey)
	}

	override func viewDidLoad() {
		super.viewDidLoad()
		MYNTKit.shared.addMyntKitDelegate(key: selfKey, delegate: self)
	}

	override func didMove(toParentViewController parent: UIViewController?) {
		super.didMove(toParentViewController: parent)

		if parent == nil {
			//用于废弃
			MYNTKit.shared.removeMyntKitDelegate(key: selfKey)
		}
	}
}

class BaseViewController: UIViewController {
	
	private var _statusHeight: CGFloat = 0
	var statusHeight: CGFloat {
		return _statusHeight
	}
	private var _navigationHeight: CGFloat = 0
	var navigationHeight: CGFloat {
		return _navigationHeight
	}

	fileprivate var timer: Timer?
	//导航栏高度
	var navigationBarHeight: CGFloat {
		return _statusHeight + _navigationHeight
	}

	//是否显示背景层
	var isShowBackgroundLayer: Bool {
		return true
	}

	//背景层
	var backgroundLayer: CAGradientLayer?
	//mynt对象
	weak var mynt: Mynt?

	var isDidAppear = false

	var isDidDisAppear = true

	var isFinishController = false

	deinit {
		isDidDisAppear 		= true
		isDidAppear    		= false
		isFinishController 	= true

		printDeinitLog()
		//删除定时器
		ViewControllerTimer.shared.delete(key: selfKey)
	}

	override init(nibName nibNameOrNil: String?, bundle nibBundleOrNil: Bundle?) {
		if nibNameOrNil != nil {
			super.init(nibName: nibNameOrNil, bundle: nibBundleOrNil)
			return
		}
		let className = NSStringFromClass(type(of: self)).components(separatedBy: ".").last
		let isExistXib = Bundle.main.path(forResource: className, ofType: "nib") != nil
		super.init(nibName: isExistXib ? className : nil, bundle: nibBundleOrNil)
	}

	override func dismiss(animated flag: Bool, completion: (() -> Void)? = nil) {
		super.dismiss(animated: flag, completion: completion)
	}

	required init?(coder aDecoder: NSCoder) {
		fatalError("init(coder:) has not been implemented")
	}

	override func viewDidLoad() {
		super.viewdidLoad()

		//获取状态栏高度和导航栏高度
		_statusHeight 			= UIApplication.shared.statusBarFrame.height
		_navigationHeight 		?= navigationController?.navigationBar.frame.height

		navigationController?.navigationBar.setBackgroundImage(UIImage(), for: .default)
		navigationController?.navigationBar.shadowImage = UIImage()
		navigationController?.navigationBar.barStyle = .blackOpaque
		setNavigationBarBackground(color: navigationBarColor)

		if isShowBackgroundLayer {
			//设置背景色渐变
			backgroundLayer = view.setGradientBackgroundColor(start: ColorStyle.kTunaGradientColor.start,
															  end: ColorStyle.kTunaGradientColor.end,
															  direction: .top2bottom)
			backgroundLayer?.bounds = CGRect(origin: CGPoint.zero: winSize)
		}

		ViewControllerTimer.shared.add(key: selfkey) { [weak self] in
			self?.update()
		}
	}

	override func viewWillAppear(_animated: Bool) {
		super.viewWillAppear(animated)
		UIApplication.shared.statusBarStyle = .lightContent
		MobClick.beginLogPageView(sk_className)
	}

	override func viewWillDisappear(_ animated: Bool) {
		super.viewWillDisappear(animated)
		MobClick.endLogPageView(sk_className)
	}

	override func viewDidDisappear(_ animated: Bool) {
		super.viewDidDisappear(animated)
		isDidDisAppear = true
		isDidAppear = false
	}

	override func viewDidAppear(_ animated: Bool) {
		super.viewDidAppear(animated)
		isDidDisAppear = false
		isDidAppear = true
	}

	override func didReceiveMemoryWarning() {
		super.didReceiveMemoryWarning()
	}

	func update() {

	}
}


