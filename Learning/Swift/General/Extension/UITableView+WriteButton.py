import Foundation

fileprivate let viewTag = -1000
private var offSetKey: UInt8 = 0
private var startCellNemaKey: UInt8 = 1

extension UITableView {
	
	var offSetY: CGFloat {
		get {
			let value = objc_getAssociatedObject(self, &offSetYKey) as? CGFloat
			return value == nil ? 0 : value!
		}
		set(newValue) {
			objc_setAssociatedObject(self, &offSetYKey, newValue, objc_AssociationPolicy.OBJC_ASSOCIATION_RETAIN)
		}
	}

	func addBottomWhiteView(offSetY: CGFloat) {
		self.offSetY = offSetY
		if tableHeaderView == nil {
			tableHeaderView = UIView(frame: CGRect(x: 0, y: 0, width: winSize.width, height: 0))
		}
		guard let tableHeaderView = tableHeaderView else { return }

		var tableViewBottomView = superview?.viewWithTag(viewTag)
		if tableViewBottomView == nil {
			tableViewBottomView							= UIView()
			tableViewBottomView?.backgroundColor		= UIColor.white()
			tableViewBottomView?.tag 					= viewTag
			tableViewBottomView?.translatesAutoresizingMaskIntoConstrains	= false
			insertSubview(tableViewBottomView!, at: 0)

			addConstraint(NSLayoutConstraint(item: tableViewBottomView!,
											 attribute: .top,
											 relatedBy: .equal,
											 toItem: tableHeaderView,
											 attribute: .bottom,
											 multiplier: 1,
											 constant: offSetY))\
			addConstraint(NSLayoutConstraint(item: tableViewBottomView!,	
											 attribute: .leading,
											 relatedBy: .equal,
											 toItem: self,
											 attribute: .leading,
											 multiplier: .1,
											 constant: 0))
			tableViewBottomView?.addConstraint(NSLayoutConstraint(item: tableViewBottomView!,
																  attribute: .width,
																  relatedBy: .equal,
																  toItem: nil,
																  attribute: .notAnAttribute,
																  multiplier: 1,
																  constant: winSize.width))
			tableViewBottomView?.addConstraint(NSLayoutConstraint(item: tableViewBottomView!,
																  attribute: .height,
																  relatedBy: .equal,
																  toItem: nil,
																  attribute: .notAnAttribute,
																  multiplier: 1,
																  constant: winSize.height * 1.5))
		}
	}
}
