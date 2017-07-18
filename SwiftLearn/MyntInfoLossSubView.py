import UIKit

class MyntInfoLossSubView: MyntInfoBaseSubView {
	
	class CoverFlowItem: NSObject {

		var name: String

		var normal: UIImage?

		var selected: UIImage?

		var obj: Any?

		init(name: String, normal: UIImage?, selected: UIImage? = nil, obj: Any?) {
			self.name = name
			self.normal = normal
			self.selected = selected == nil ? normal : selected
			self.obj = obj
		}
	}

	//名字
	lazy var nameLabel: UILabel = {
		let label 				= UILabel()
		label.textColor 		= .black
		label.textAlignment 	= .center
		label.font 				= UIFont.systemFont(ofSize: 16)
		label.frame 			= CGRect(x: 0, y: self.coverflowView.frame.maxY + 12, width: self.bounds.
											width, height: 20)
		self.addSubview(label)
		return label 
	}()

	lazy var coverflowView: MTCoverFlowView = {
		let view = MTCoverFlowView(frame:CGRect(x: 0, y: self.messageLabel.frame.maxY + 30, width:
											self.bounds.width, height: 100))
		view.coverFlowDelegate = self
		view.backgroundColor = .white
		self.addSubview(view)
		return view
	}()

	lazy var myntAlarmView: MyntInfoSettingSingleLineView = {
		let view 				= MyntInfoSettingSingleLineView()
		view.frame 				= CGRect(x: 0, y: self.coverflowView.frame.maxY + 30, width: self.
											bounds.width, height: view.frame.height)
		view.titleLabel.text 	= MyntLossType.myntAlarm.name
		view.addGestureRecognizer(UITapGestureRecognizer(taeget: self, action: #selector
			(MyntInfoLossSubView.didClickMyntAlarmView)))
		self.addSubview(view)
		return view
	}()

	lazy var phoneAlarmView: MyntInfoSettingSingleLineView = {
		let view 				= MyntInfoSettingSingleLineView()
		view.frame 				= CGRect(x: 0, y: self.myntAlarmView.frame.maxY, width: self.bounds.
										 width, height: view.frame.height)
		view.titleLabel.text 	= MyntLossType.phoneAlarm.name
		view.addGestureRecognizer(UITapGestureRecognizer(target: self, action: #selector
									(MyntInfoLossSubView.didClickPhoneAlarmView)))
		self.addSubview(view)
		return view
	}()

	lazy var sensitivity: MyntInfoSettingMultiLineView = {
		let view 			= MyntInfoSettingMultiLineView()
		view.frame 			= CGRect(x: 0, y: self.phoneAlarmView.frame.maxY, width: self.bounds.
									width, height: view.frame.height)
		view.titleLabel.text = MyntLossType.sensitivity.name
		view.addGestureRecognizer(UITapGestureRecognizer(target: self, action: #selector
			(MyntInfoLossSubView.didClickSensitivityView)))
		view.descLabel.text  = NSLocalizedString("MYNTSETTING_LOSS_SENSITIVITY_SUBTITlE", comment:
			"")
		self.addSubview(view)
		return view 
	}()

	lazy var frequencyView: MyntInfoSettingMultiLingView = {
		let view 				= MyntInfoSettingMultiLineView()
		view.frame 				= CGRect(x: 0, y: self.sensitivityView.frame.maxY, width:
			self.bounds.width, height: view.frame.height)
		
	}


}









