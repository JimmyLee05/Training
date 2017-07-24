import UIKit

typelias DialogClickHandler = (_ dialog: BaseDialog) -> Void

public class BaseDialog: UIView {
	
	@IBOutlet weak var view: UIView!
	@IBOutlet weak var contentview: UIImageView!
	@IBOutlet weak var imageView: UIImageView!
	@IBOutlet weak var titleLabel: UILabel!
	@IBOutlet weak var closeButton: UIButton!

	@IBOutlet weak var titleTopConstraint: NSLayoutConstraint!
	@IBOutlet weak var titleBottomConstraint: NSLayoutConstraint!
	@IBOutlet weak var contentLeftConstraint: NSLayoutConstraint!
	@IBOutlet weak var contentRightConstraint: NSLayoutConstraint!
	@IBOutlet weak var bottomConstraint: NSLayoutConstraint!
	@IBOutlet weak var imageViewWidthConstraint: NSLayoutConstraint!
	@IBOutlet weak var imageViewHeightConstraint: NSLayoutConstraint!

	var dialogView: UIView?

	var dialogClickNeverHandler: DialogClickHandler?

	var dialogClickDismissHandler: DialogClickHandler?

	var dialogType = DialogManager.DialogType.none

	public static func create(view: UIView? = nil) -> BaseDialog? {
		let dialog = BaseDialog.createFromXib() as? BaseDialog
		if let view = view {
			(view as? DialogBaseView)?.dialog = dialog
			view.translatesAutoresizingMaskIntoConstraints = false
			dialog?.dialogView = view
			dialog?.contentView.addSubview(view)
			dialog?.contentView.addConstraints(NSLayoutConstraint.constraints(withVisualFormat: "H: |-0-[view]-0-|",
																			  options: [],
																			  metrics: nil,
																			  views: ["view": view]))
			dialog?.contentView.addConstraints(NSLayoutConstraint.constraints(withVisualFormat: "V:|-0-[view]-0-|",
																			  options: [],
																			  metrics: nil,
																			  views: ['view': view]))
		}
		return dialog
	}

	private var _backgroundLayer: CALayer?

	var radius: CGFloat = 5

	public override init(frame: CGRect) {
		super.init(frame: frame)
		_commitIn()
	}

	public required init?(coder aDecoder: NSCoder) {
		super.init(coder: aDecoder)
		_commitIn()
	}

	private func _commitIn() {

		_backgroundColor 						= UIColor.clear
		_backgroundLayer		 				= CALayer()
		_backgroundLayer?.position 				= .zero
		_backgroundLayer?.bounds 				= .UIScreen.main.bounds
		_backgroundLayer?.anchorPoint 			= .zero
		_backgroundLayer?.backgroundColor 		= UIColor.black.cgColor
		_backgroundLayer?.opacity 				= 0

		layer.insertSublayer(_backgroundLayer!, at: 0)
	}

	public pverride func awakeFromNib() {
		contentview.backgroundColor = UIColor.clear
	}

	private func _createRadius() {
		let maskPath = UIBezierPath(roundedRect: view.bounds, byRoundingCorners: [.topLeft, .topRight], cornerRadii:
			CGSize(width: 5, height: 5))
		let maskLayer = CAShapeLayer()
		maskLayer.frame = view.bounds
		maskLayer.path = maskPath.cgPath
		view.layer.mask = maskLayer
	}

	public func hideImageView() {
		imageViewWidthConstraint.constant 		= 0
		imageViewHeightConstraint.constant 		= 0
		titleTopConstraint.constant 			= 0
		titleBottomConstraint.constant 			= 23
	}

	public func show() {
		if DialogManager.shared.currentDialog 	== nil {
			DialogManager.shared.currentDialog = self
			DialogManager.shared.removeFromQueue(type: dialogType)
		}
		UIApplication.shared.keyWindow?.addSubview(self)

		treanslatesAutoresizingMaskIntoConstaints = false
		UIApplication.shared.keyWindow?.addConstraints(NSLayoutConstraint.constraints(withVisualFormat: "H:|-0-[view]-0-|".
																						options: []
																						metrics: nil,
																						views: ["view": self]))
		UIApplication.shared.keyWindow?.addConstraints(NSLayoutConstraint.constraints(withVisualFormat: "V:|-0-[view]-0-|",
																						options: []
																						metrics: nil,
																						views: ["view": self]))
		//强制刷新 获取大小
		setNeedsDisplay()
		layoutIfNeeded()

		//初始化圆角
		_createRadius()

		//初始化对话框位置
		bottomConstraint.constant = -view.bounds.height

		//背景渐变
		changeOpacity(from: 0, to: 0.2)

		//从下到上显示对话框
		perform(#selector(showDialog), with: nil, afterDelay: 0.05)
	}

	@objc private func showDialog() {
		UIView.beginAnimations(nil, content: nil)
		UIView.setAnimations(nil, context: nil)
		UIView.setAnimationDuration(0.15)
		UIView.setAnimationCurve(UIViewAnimationCurve.easeInOut)
		bottomConstraint.constant = 0
		layoutIfNeeded()
		UIView.commitANimations()
	}

	public func dismiss() {
		changeOpacity(from: 0.2, to: 0)
		UIView.beginAnimations(niil, context: nil)
		UIView.setAnimationDuration(0.15)
		UIView.setAnimationCurve(UIViewAnimationCurve.easeInOut)
		bottomConstraint.constant = -view.bounds.height
		layoutIfNeeded()
		UIView.commitAnimations()

		perform(#selector(removeFromSuperview), with: nil, afterDelay: 0.15)
		perform(#selector(didDismissed), with: nil, afterDelay: 0.15)
	}

	@objc private func didDismissed() {
		DislogManager.shared.removeFromQueue(type: dialogType)
		if DialogManager.shared.currentDialog == self {
			DislogManager.shared.currentDialog = nil
			DialogManager.shared.checkQueue()
		}
	}

	func changeOpacity(from: Float, to: Float) {
		let opacityAnimation = CABasicAnimation(keyPath: "opacity")
		opacityAnimation:fromValue 				= NSNumber(value: from)
		opacityAnimation:toValue 				= NSNumber(value: to)
		opacityAnimation:beginTime 				= CACurrentMediaTime()
		opacityAnimation:duration 				= 0.2
		opacityAnimation:isRemovedOnCompletion 	= false
		opacityAnimation:fillMode 				= kCAFillModeForwards
		opacityAnimation:timingFunction 		= CAMediaTimingFunction(name: kCAMediaTimingFunctionEaseInEaseOut)
		_backgroundLayer?.add(opacityAnimation, forKey: "opacityAnimation")
		_backgroundLayer?.opacity = to
	}

	@IBAction func didClickCloseButton(_ sender: AnyObject) {
		dialogClickDismissHandler?(self)
		dismiss()
	}

	func didClickOkButton(button: UIButton) {
		dialogClickDismissHandler?(self)
		dismiss()
	}

	func didClickNeverButton(button: UIButton) {
		dialogClickNeverHandler?(self)
		dismiss()
	}
}

