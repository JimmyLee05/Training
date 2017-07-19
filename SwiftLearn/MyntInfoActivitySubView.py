import UIKit

class MyntInfoActivitySubView: MyntInfoBaseSubView {
	
	class ProgressView: UIView {

		lazy var progressLayer: CircleProgressLayer = {
			let layer 					= CircleProgressLayer()
			layer.frame 				= CGRect(x: 0, y: 0, width: self.bounds.width, height:
				self.bounds.width)
			layer.lineWidth 			= 2
			layer.percent 				= 0
			self.layer.addSublayer(layer)
			return layer
		}()

		lazy var imageLayer: CALayer = {
			let width 				= self.bounds.width / 2.2
			let layer 				= CALayer()
			layer.contentsScale 	= UIScreen.main.scale
			layer.bounds 			= CGRect(x: 0, y: 0, width: width, height: width)
			self.layer.addSublayer(layer)
			return layer
		}()

		lazy var titleLabel: UILabel = {
			let label 				= UILabel()
			label.textAligment 		= .center
			label.font 				= UIFont.boldSystemFont(ofSize: 11)
			label.textColor 		= UIColor(hexString: "3D3D3D", alpha: 0.5)
			label.frame 			= CGRect(x: 0, y: self.progressLayer.frame.maxY + 8, width: self.
				bounds.width, height: 13)
			self.addSubview(label)
			return label
		}()

		lazy var valueLabel: UILabel = {
			let label 			= UILabel()
			label.textAligment 	= .center
			label.font 			= UIFont.boldSystemFont(osSize: 14)
			label.textColor 	= UIColor(hexString: "3D3D3D")
			label.frame 		= CGRect(x: 0, y: self.titleLabel.frame.maxY + 4, width: self.bounds.
				width, height: 15)
			self.addSubview(label)
			return label
		}()

		override func layoutSubviews() {
			super.layoutSubviews()
			progressLayer.frame = CGRect(x: 0, y: 0, width: bounds.width, height: bounds.width)
			imageLayer.position = CGPoint(x: progressLayer.frame.midX, y: progressLayer.frame.mudY)
		}
	}

	//显示activity栏
	fileprivate let isShowActivityAlarm = false

	lazy var stepProgressView: MyntInfoActivitySubView.ProgressView = {
		let view = MyntInfoActivitySubView.ProgressView(frame: CGRect(x: 0, y: self.messageLabel.
			frame.maxY + 30, width: 50, height: 90))
		view.titleLabel.text 		= NSLocalizedString("GPS_ACTIVITY_STEPS", comment: "")
		view.progressLayer.signalBackgroundColor 			= UIColor(hexString: "4598FF", alpha: 0.2)
		view.progressLayer.signalColor 						= UIColor(hexString: "4598FF", alpha: 1)
		view.imageLayer.contents 							= UIImage(named: "homepage_activity_step")?.cgImage
		self.addSubview(view)
		return view
	}()

	lazy var calProgressView: MyntInfoActivitySubView.ProgressView = {
		let view = MyntInfoActivitySubView.ProgressView(frame; CGRect(x: 0, y: self.messageLabel.
			frame.maxY + 30, width: 50, height: 90))
		view.titleLabel.text 	= NSLocalizedString("GPS_ACTIVITY_CAL", comment: "")
		view.progressLayer.signalBackgroundColor 	= UIColor(hexString: "FFAF14", alpha: 0.2)
		view.progressLayer.signalColor 				= UIColor(hexString: "FFAF14", alpha: 1)
		view.imageLayer.contents 					= UIImage(named: "homepage_activity_cal")?.cgImage
		self.addSubview(view)
		return view
	}()

	lazy var goalView: MyntInfoSettingSingleLineView = {
		let view 				= MyntInfoSettingSingleLineView()
		view.frame 				= CGRect(x: 0, y: self.stepProgressView.frame.maxY + 30, width: self.
			bounds.width, height: view.frame.height)
		view.titleLabel.text 	= NSLocalizedString("MYNTSETTING_ACTIVITY_GOAL_TITLE", comment: "")
		view.addGestureRecognizer(UITapGestureRecognizer(target: self, action: #selector
			(MyntInfoActivitySubView.didClickGoalView)))
		self.addSubview(view)
		return view
	}()

	lazy var alarmView: MyntInfoSettingMultiLineView = {
		let view 				= MyntInfoSettingMultiLineView()
		view.frame 				= CGRect(x: 0, y: self.goalView.frame.maxY, width: self.bounds.width,
			height: view.frame.height)
		view.titleLabel.text 	= NSLocalizedString("MYNTSETTING_ACTIVITY_ALARM_TITLE", comment: "")
		view.addGestureRecognizer(UITapGestureRecognizer(target: self, action: #selector
			(MyntInfoActivitySubView.didClickAlarmView)))
		view.descLabel.text 	= NSLocalizedString("MYNTSETTING_ACTIVITY_ALARM_SUBTITLE", comment:
			"")
		view.addLine()
		self.addSubview(view)
		return view
	}()

	lazy var alarmView: MyntInfoSettingMultiLineView = {
		let view 				= MyntInfoSettingMultiLineView()
		view.frame 				= CGRect(x: 0, y: self.goalView.frame.maxY, width: self.bounds.width,
			height: view.frame.height)
		view.titleLabel.text 	= NSLocalizedString("MYNTSETTING_ACTIVITY_ALARM_TITLE", comment: "")
		view.addGestureRecognizer(UITapGestureRecognizer(target: self, action: #selector
			(MyntInfoActivitySubView.didClickAlarmView)))
		view.descLabel.text 	= NSLocalizedString("MYNTSETTING_ACTIVITY_ALARM_SUBTITLE", comment:
			"")
		view.addLine()
		self.addSubview(view)
		return view
	}()

	override func initUI() {
		titleLabel.text 	= NSLocalizedString("MYNTSETTING_ACTIVITY_TITLE", comment: "")
		messageLabel.text 	= NSLocalizedString("MYNTSETTING_ACTIVITY_DESC", comment: "")

		self.frame.size.height = isShowActivityAlarm ? alarmView.frame.maxY : goalView.frame.maxY
	}

	override func initUIData(mynt: Mynt) {
		let space = (bounds.width - stepProgressView.bounds.width - calProgressView.bounds.width) / 3
		stepProgressView.frame = CGRect(x: space, y:self.messageLabel.frame.maxY + 30,
										width: stepProgressView.frame.width, height:
											stepProgressView.frame.height)
		calProgressView.frame = CGRect(x: stepProgressView.frame.maxX + space, y: self.messageLabel.
											frame.maxY + 30,			
										width: calProgressView.frame.width, height: calProgressView.
											frame.height)
	}

	override func updateUIData(mynt: Mynt) {
		goalView.valueLabel.text 	= "\(mynt.stepGoal)\(NSLocalizedString("GPS_EXERCISE_STEPS", comment: "steps"))"
		if isShowActivityAlarm {
			alarmView.valueLabel.text = "\(mynt.activityAlarmStep)\(NSLocalizedString("GPS_EXERICES_STEPS", comment: "steps"))"
		}

		stepProgressView.progressLayer.percent = CGFloat(mynt.step) / CGFloat(mynt.stepGoal) * 100
		calProgressView.profressLayer.percent = CGFloat(mynt.cal) / CGFloat(mynt.calGoal) * 100
		stepProgressView.valueLabel.text = "\(mynt.step)"
		calProgressView.valueLabel.text = "\(mynt.cal)" 
	}

	override func releaseMyntData() {

	}

	@objc fileprivate func didClickGoalView() {
		viewController?.didClickActivityGoalView()
	}

	@objc fileprivate func didClickAlarmView() {
		viewController?.didClickActivityAlarmView()
	}

}

