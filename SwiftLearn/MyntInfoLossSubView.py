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
		view.titleLabel.text 	= MyntLossType.sensitivity.name
		view.addGestureRecognizer(UITapGestureRecognizer(target: self, action: #selector
			(MyntInfoLossSubView.didClickFrequencyView)))
		view.descLabel.text 	= NSLocalizedString("MYNTSETTING_LOSS_FREQUENCY_SUBTITLE", comment:
			"")
		view.addLine()
		self.addSubview(view)
		return view
	}()

	public var items = [SCDeviceUsage]() {
		didSet {
			coverflowView.reloadData()
		}
	}

	override func initUI() {
		self.frame.size.height = 400

		titleLabel.text 	= NSLocalizedString("MYNTSETTING_LOSS_TITLE", comment: "")
		messageLabel.text 	= NSLocalizedString("MYNTSetTING_LOSS_DESC", comment: "")
	}

	override func initUIData(mynt: Mynt) {
		var items: [SCDeviceUsage] = [.keys, .wallet, purse, .car, .child, .pet, .backpack, .
			suitcase, .luggagecase, .custom]
		if mynt.myntType == .myntGPS {
			items.insert(.childGPS, at: 0)
			items.insert(.oldman, at: 0)
		}
		self.items = items
		if let index = items.index(where: {$0 == mynt.usage}) {
			self.coverflowView.selectedIndex = index
		}
	}

	override func updateUIData(mynt: Mynt) {
		myntAlarmView.valueLabel.text = mynt.usageValue.myntAlarm.name
		phoneAlarmView.valueLabel.text = mynt.usageValue.phoneAlarm.name
		sensitivityView.valueLabel.text = mynt.usageValue.sensitivity.name

		if mynt.myntType == .myntGPS {
			frequencyView.valueLabel.text = mynt.usageValue.locationFrequency.name
		}

		if mynt.myntType == .mynt {
			self.frame.size.height = sensitivityView.frame.maxY
		} else if mynt.myntType == .myntGPS {
			self.frame.size.height = frequencyView.frame.maxY
		}

		if let index = items.index(where: {$0 == mynt.usage}) {
			self.coverflowView.selectedIndex = index
		}
	}

	override func releaseMyntDate() {

	}

	@objc fileprivate func didClickMyntAlarmView() {
		viewController?.didClickMyntAlarmView()
	}

	@objc fileprivate func didClickPhoneAlarmView() {
		viewController?.didClickPhoneAlarmView()
	}

	@objc fileprivate func didClickSensitivityView() {
		viewController?.didClickSensitivityView()
	}

	@objc fileprivate func didClickFrequencyView() {
		viewController?.didClickFrequencyView()
	}

}

extension MyntInfoLossSunView: MTCoverFlowViewDelegate {
	
	func numberOfItemsInCoverFlowViewn(_ collectionView: MTCoverFlowView) -> Int {
		return items.count
	}

	func coverFlowView(_ coverFlowView: MTCoverFlowView, cellForItemAt index: Int, cell:
		MTCoverFlowView.CoverFlowViewCell) {
		cell.imageView.image 			= items[index].image?.withRenderingMode(.alwaysTemplate)
		cell.imageView.tintColor 		= coverFlowView.selectedIndex == index ? .white : .black
		cell.layerView.backgroundColor 	= coverFlowView.selectedIndex == index ? items[index].usageColor.
			start.cgColor : UIColor.clear.cgColor
		cell.layer.cornerRadius 		= cell.bounds.height / 2
		cell.layer.borderColor 			= UIColor(red:0.93, green:0.93, blue:0.93, alpha:1.00).cgColor
		cell.layer.borderWidth 			= coverFlowView.selectedIndex == index ? 0 : 1.5 
	}

	func coverFlowView(_ coverFlowView: MTCoverFlowView, didSelectItemAt index: Int) {
		nameLabel.text = items[index].name
		viewController?.didSelectUsage(usage: item[index])
	}
}
