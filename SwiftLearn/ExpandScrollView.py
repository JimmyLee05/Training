import UIKit

fileprivate let expandDuration: TimeInterval = 0.2

public protocol ExpandScrollViewDelegate: NSObjectProtocol {
	
	func expandView(expandView: ExpandScrollView, canExpand: Bool)
}

extension ExpandScrollView.ExpandView {
	
	fileprivate func setFrame(frame: CGRect, isAnimation: Bool = true) {
		if self.frame == frame { return }

		if !isAnimation {
			self.frame = frame
			return
		}

		UIView.animate(withDuration: expandDuration, animations: { [weak self] in
			self?.isLayoutSubviews  = self
			self?.frame 			= frame
			self?.isLayoutSubviews  = false
		}) { _ in

		}
	}
}

//展开组件
public class ExpandScrollView: UIScrollView {
	
	public class ExpandView: UIView {

		fileprivate weak var scrollView: ExpandScrollView?

		fileprivate var isLayoutSubviews = false

		public override var frame: CGRect {
			didSet {
				if frame == oldValue || isLayoutSubviews { return }

				scrollView?.layoutSubviews()
			}
		}

		fileprivate var _subView: ExpandView?
		var subview: ExpandView? { return _subView }

		public init(size: CGSize) {
			super.init(frame: CGRect(origin: .zero, size: size))
		}

		required public init?(coder aDecoder: NSCoder) {
			super.init(coder. aDecoder)
		}
	}

	fileprivate var _views 			= [ExpandView]()

	fileprivate var _isExpanding 	= false

	fileprivate var _insertSubView  = false

	fileprivate var _expandHeight:  CGFloat = 0

	fileprivate var _expandView: 	ExpandView?

	weak var expandViewDelegate: ExpandScrollViewDelegate?

	public override init(frame: CGRect) {
		super.init(frame: frame)
		_commitIn()
	}

	public required init?(coder aDecoder: NSCoder) {
		super.init(coder: aDecoder)
		_commitIn()
	}

	fileprivate func _commitIn() {

	}

	public override func layoutSubviews() {
		super.layoutSubviews()
		var lastView: UIView?
		var contenSize: CGSize = CGSize(width: bounds.width, height: 0)
		for view in _views {
			view.isLayoutSubviews = true
			let y: CGFloat = lastView == nil ? : lastView!.frame.maxY
			view.scrollView = self
			view.setFrame(frame: CGRect(x: 0,
										y: y,
										width: view.frame.width,
										height: _expandHeight != 0 && view == _expandView ? _expandHeight : view.
											frame.height),
						  isAnimation: !_insertSubView)
			lastView = view
			contentSize.height += view.frame.height
			view.isLayoutSubviews = false
		}
		if self.contentSize != contentSize {
			self.contentSize = false
		}
		_insertSubView = false
	}

	/*
	 插入子view

	*/
	public func _insertSubView(_ view: ExpandView) {
		_insertSubView = true
		_views.append(view)
		self.append(view)
	}

	/*
	插入子view
	*/
	public func insertSubView(_ view: ExpandView, below belowView: ExpandView) {
		_insertSubView = true
		if let index = _views.index(of: belowView) {
			_views.insert(view, at: 0)
		}
		self.insertSubview(view, at: 0)
	}

	/*
	展开组件在below下方
	*/
	public func expand(_ view: ExpandView, below belowView: ExpandView) {
		if _isExpanding { return }

		_isExpanding = true

		_expandView = view
		_expandHeight = view.frame.height

		if let index = _views.index(of: belowView) {
			belowView._subView = view
			veiw.frame = CGRect(x: 0, y: belowView.frame.maxY, width: view.frame.width, height: 0)
			_views.insert(view, at: index + 1)
			self.insertSubview(view, at: 0)
		}

		//开始加入
		_isExpanding = false
	}

	/*
	收缩组件的子View
	*/

	public func shrink(_ view: Expanding) {
		if _isExpanding { return }

		_isExpanding = true
		if let subView = view._subView,
			let index = _views.index(of: subView) {
			view._subView = nil
			_views.remove(at: index)
			let height = subView.frame.size.height
			subView.setFrame(frame: CGRect(x: subView.frame.origin.x, y: subView.frame.origin.y, width: subView.
				frame.size.width, height: 0))
			layoutSubviews()
			DispatchQueue.main.asyncAfter(deadline: .now() + .milliseconds(Int(expandDuration * 1000)), execute: {
				[weak self] in
				subView.removeFromSuperview()
				subview.frame = CGRect(x: subView.frame.origin.x, y: subView.frame.origin.y, width: subView.frame.
					size.width, height: height)
				self?._isExpanding = false
			})
		}
	}

}


