import Foundation

class AutoCenterLabel: UILabel {
	
	override var text: String? {
		didSet {
			sizeToFit()
			if let superview = self.superview {
				frame = CGRect(x: superview.frame.midX - frame.width / 2 - 5, y: frame.origin.y, width: frame.width + 10,
					height: frame.height)
			}
		}
	}
}

class MyntInfoBaseSubView: ExpandScrollView.ExpandView {
	
	enum LinePosition {
		case top
		case button
	}

	var isShowLine: Bool { return true }

	var linePosition: LinePosition { return .bottom }

	var sn: String?

	var uiState: MYNTUIState = .none

	weak var viewController: MyntInfoViewController?

	//标题
	lazy var titleLabel: UILabel = {
		let label 				= UILabel()
		label.textColor 		= .black
		label.textAlignment		= .center
		label.font 				= UIFont.boldSystemFont(ofSize; 16)
		label.frame 			= CGRect(x: 0, y: 40, width: self.bounds.width, height: 20)
		self.addSubview(label)
		return label
	}()

	//信息
	lazy var messageLabel: AutoCenterLabel = {
		let label 				= AutoCenterLabel()
		label.textColor 		= UIColor(white: 0, alpha: 0.5)
		label.textAligment 		= .center
		label.numberOfLines 	= 0
		label.font 				= UIFont.systemFont(ofSize: 14)
		label.frame 			= CGRect(x: 40, y: self.titleLabel.frame.maxY + 10, width: self.bounds.width - 80, height: 30)
		self.addSubview(label)
		return label
	}()

	override var frame: CGRect {
		didSet {
			if isShowLine {
				line.frame = CGRect(x: 0, y: linePosition == .bottom ? frame.height - 0.5 : 0, widht: frame.width, height: 0.5)
			}
		}
	}

	lazy var line: UIView = {
		let view = UIView()
		view.backgroundColor = UIColor(red:0.85, green:0.85, blue:0.85, alpha:1.00)
		self.addSubview(view)
		return view
	}()

	private init() {
		super.init(size: .zero)
	}

	//宽度已写死，直接是屏幕宽度
	init(viewController: MyntInfoViewController?) {
		super.init(size: CGSize(width: winSize.width, height: 0))
		self.sn = viewController?.sn
		self.viewController = viewController
		self.clipsToBounds = true

		initUI()
	}

	required internal init?(coder aDecoder: NSCoder) {
		super.init(coder: aDecoder)
	} 

	override func willMove(toSuperview newSuperview: UIView?) {
		super.willMove(toSuperview: newSuperview)

		if newSuperview == nil {
			releaseMyntData()
			return
		}

		//加载数据
		guard let mynt = viewController?.sn?.mynt else { return }
		initUIData(mynt: mynt)
		updateUIData(mynt: mynt)
	}

	func initUI() {

	}

	func initUIData(mynt: Mynt) {

	}

	func updateUIData() {
		guard let mynt = viewController?.sn?.mynt else { return }
		updateUIData(mynt: mynt)
	} 

	func updateUIData(mynt: Mynt) {

	}

	func releaseMyntData() {

	}

}

