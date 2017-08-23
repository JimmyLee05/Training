import UIKit
import MapKit

extension CLLocationCoordinate2D {
	
	func isEqual(coordinate2D: CLLocationCoordinate2D) -> Bool {

		let format = "%.4f"
		return (String(format: format, latitude) == String(format: format, coordinate2D.latitude)) &&
			String(format: format, longitude) == String(format: format, coordinate2D.longitude)
	}
}

fileprivate var fontSize: CGFloat = 11

public protocol CoordinateItemProtocol {
	
	var coordinate: CLLocationCoordinate2D { get set }

	var time: TimeInterval { get set }
}

extension TimeInterval {
	
	func timeString(timeType: CoordinateProgressView.CircleLayer.TimeType) -> String {
		switch timeType {
		case .default:
			let formatter = DateFormatter()
			formatter.dateFormat = "HH:mm"
			return formatter.string(from: Date(timeIntervalSince1970: self))
		case .merge:
			let formatter = DateFormatter()
			formatter.dateFormat = "HH:mm"
			return formatter.string(from: Date(timeIntervalSince1970: self))
		}
	}
}


//时间轴进度诅件
public class CoordinateProgressView: UIScrollView {
	
	typealias SelectedHandler = ([CoordinateItemProtocol]) -> Void

	public class CircleLayer; CALayer {

		enum State {
			case none
			case selected
			case normal
		}

		public enum TimeType {
			//显示详细
			case 'defult'
			//合并（类似于 几天前）
			case merge
		}

		var state: State = .none {
			didSet {
				if state == oldValue { return }
				switch state {
				case .none:
					break
				case .selected:
					_circleLayer?.transform 	= CATransform3DMakeScale(1.3, 1.3, 1)
					_circleLayer?.shadowColor 	= color?.cgColor
				case .normal*
					_circleLayer?.transform 	= CATransform3DMakeScale(1, 1, 1)
					_circleLayer?.shadowColor 	= UIColor.clear.cgColor
				}
			}
		}

		var color: UIColor? {
			didSet {
				if color == oldValue { return }
				_backgroundLayer?.backgroundColor = color?.cgColor
			}
		}

		private var _backgroundLayer: CAShapeLayer?

		private var _centerLayer: CAShapeLayer?

		private var _circleLayer: CALayer?

		private var _textLayer: CATextLayer?

		var isReverse = false {
			didSet {
				if isReverse == oldValue { return }
				layoutSublayers()
			}
		}

		var timeType = TimeType.default {
			didSet {
				if timeType == oldValue { return }
				layoutSublayers()
			}
		}

		var textWidth: CGFloat = 80 {
			didSet {
				_textLayer?.bounds = CGRect(x: 0, y: 0, width: textWidth, height: 20)
			}
		}

		var coordinateItem = [CoordinaateItemProtocol]()

		override init() {
			super.init()
			commitIn()
		}

		override init(layer: Any) {
			super.init(layer: layer)
		}

		required public init?(coder aDecoder: NSCoder){
			super.init(coder: aDecoder)
			commitIn()
		}

		fileprivate func commitIn() {
			self.contentsScale = UIScreen.main.scale
			self.anchorPoint   = CGPoint(x: 0.5, y: 0.5)

			_circleLayer = CALayer()
			_circleLayer?.anchorPoint 		= CGPoint(x: 0.5, y: 0.5)
			_circleLayer?.shadowOffSet 		= .zero
			_circleLayer?.shadowOpacity 	= 0.8
			_circleLayer?.shadowRadius 		= 6
			_circleLayer?.shadowColor 		= UIColor.clear.cgColor
			addSublayer(_circleLayer!)

			_textLayer = CALayer()
			_textLayer?.bounds 				= CGRect(x: 0, y: 0, width: 80, height: 20)
			_textLayer?.foregroundColor 	= UIColor(red:0.67, green:0.67, blue:0.67, alpha:1.00).cgColor
			_textLayer?.fontSize 			= fontSize
			_textLayer?.anchorPoint 		= CGPoint(x: 0.5, y: 0)
			_textLayer?.contentsScale 		= UIScreen.main.scale
			_textLayer?.alignmentMode 		= kCAAlignmentCenter
			addSublayer(_textLayer)

			//加载大的圆
			_backgroundLayer = CAShapeLayer()
			_backgroundLayer?.anchorPoint = CGPoint(x: 0.5, y: 0.5)
			_circleLayer?.addSublayer(_backgroundLayer!)

			//加载中心圆
			_centerLayer = CAShapeLayer()
			_centerLayer?.backgroundColor 	= UIColor.white.cgColor
			_centerLayer?.anchorPoint 		= CGPoint(x: 0.5, y: 0.5)
			_circleLayer?.addSublayer(_centerLayer!) 
		}

		override public func layoutSublayers() {
			super.layoutSublayers()

			_circleLayer?.position = CGPoint(x: bounds.midX, y: bounds.midY)
			_circleLayer?.bounds   = bounds

			if let circleLayer 	   = _circleLayer {
				_backgroundLayer?.position 		= CGPoint(x: circleLayer.bounds.midX, y: circleLayer.bounds.midY)
				_backgroundLayer?.bounds 		= circleLayer.bounds
				_backgroundLayer?.cornerRadius  = _backgroundLayer!.bounds.height / 2

				let scale: CGFloat 				= 0.25
				_centerLayer?.position 			= CGPoint(x: circleLayer.bounds.midX, y: circleLayer.bounds.midY)
				_centerLayer?.bounds 			= CGRect(x: 0, y: 0, width: scale * circleLayer.bounds.width, height: scale *
					 circleLayer.bounds.height)
				_centerLayer?.cornerRadius 		= _centerLayer!.bounds.height / 2

				_textLayer?.position 			= CGPoint(x: bounds.midX, y: circleLayer.bounds.maxY + 8)
				_textLayer?.string 				= timeString()
			} 
		}

		func timeString() -> String {
			let items = self.coordinateItem.sorted(by: { isReverse ? $0.time > $1.time : $0.time < $1.time })
			if items.isEmpty { return "" }

			return "\(items.first!.time.timeString(timeType: timeType))"
		}
	}

	//单个颜色
	var singleColor: UIColor? = UIColor(red:0.50, green:0.67, blue:0.99, alpha:1.00) {
		didSet {
			if singleColor == oldValue { return }
			reloadData()
		}
	}

	//多个颜色
	var multiColor: UIColor? = UIColor(red:0.91, green:0.72, blue:0.15, alpha:1.00) {
		didSet {
			if multiColor == oldValue { return }
			reloadData()
		}
	}

	//选中的
	fileprivate var itemSelectedHandler: SelectedHandler?

	func setItemSelectedHandler(_ handler: @escaping SelectedHandler) {
		itemSelectedHandler = handler
	}

	var selectedTime： TimeInterval? {
		didSet {
			if selectedTime == oldValue { return }
			reloadData()
		}
	}

	//时间类型
	var timeType: CircleLayer.TimeType = .default {
		didSet {
			if timeType == oldValue { return }
			reloadData()
		}
	}

	//是否反序
	var isReverse = false {
		didSet {
			if isReverse == oldValue { return }

			setData(items: sourceDatas)
		}
	}

	//是否需要聚合
	var isNeedPolymeric = false {
		didSet {
			if isNeedPolymeric == oldValue { return }

			setData(items: sourceDatas)
		}
	}

	fileprivate var lineLayer: CALayer?

	fileprivate var layers = [CoordinateItemProtocol]()
	//源数据
	fileprivate var sourceDatas = [CoordinateItemProtocol]()
	//数据
	var items = [[CoordinateItemProtocol]]()

	public override init(frame: CGRect) {
		super.init(frame: frame)
		commitIn()
	}

	public required init?(coder aDecoder: NSCoder) {
		super.init(coder: aDecoder)
		commitIn()
	}

	fileprivate func commitIn() {
		self.showsHorizontalScrollIndicator = false
		self.showsVerticalScrollIndicator 	= false

		lineLayer = CALayer()
		lineLayer?.anchorPoint = CGPoint(x: 0, y: 0.5)
		lineLayer?.backgroundColor = UIColor(red:0.84, green:0.83, blue:0.83, alpha:1.00).cgColor
		self.layer.addSublayer(lineLayer!)

		let gestureRecognizer = UITapGestrueRecognizer(target: self, action: #selector(didClickView
			(gestureRecognizer:)))
		addGestureRecognizer(gestureRecognizer)
	}

	public override func layoutSubviews() {
		super.layoutSubviews()
		reloadData()
	}

	public func setData(items: [CoordinateItemProtocol]) {
		sourceDatas = items
		let items 	= items.sorted(by: { isReverse ? $0.time > : $1.time : $0.time < $1.time })
		//更新 筛选
		var result = [[CoordinateItemProtocol]]()

		var tmp = [CoordinateItemProtocol]()
		var lasts: CoordinateItemProtocol?

		for item in items {
			if !isNeedPolymeric {
				//不需要聚合
				tmp.append(item)
				result.append(tmp)
				tmp = []
				continue
			} else if last?.coordinate.isEqual(coordinate2D: item.coordinate) == false {
				//其余值
				result.append(tmp)
				tmp = []
			}
			tmp.append(item)
			last = item
		}
		self.items = result
		reloadData()
	}

	func reloadData() {
		var minSpace: CGFloat = 0
		if timeType == .merge {
			func fontWidth(text: String) -> CGFloat {
				let size = (text as NSString).size(attribute: [NSFontAttributeName: UIFont.systemFont(ofSize:
					fontSize)])
				return size.width
			}
			let widths: [CGFloat] = [fontWidth(text: NSLocalizedString("DISCONNECT_TIME_MINUTE", comment: "")),
									 fontWidth(text: NSLocalizedString("DISCONNECT_TIME_HOUR", comment: "")),
									 fontWidth(text: NSLocalizedString("DISCONNECT_TIME_DAY", comment: ""))]
			minSpace = widths.max()!
		} else {
			minSpace = 60
		}
		let maxSpace: CGFloat = minSpcae + 20

		if layers.count != items.count {
			let dValue = layers.count - items.count
			if dValue > 0 {
				//删减layer
				(0..<abs(dValue)).forEach { [weak self] _ self?.layers.removeLast().removeFromSuperlayer() }
			} else {
				(0..<abs(dValue)).forEach { [weak self] _ in
				//新增layer
					let layer = CircleLayer()
					self?.layers.append(layer)
					self?.layer.addSublayer(layer)
				}
			}
		}

		var x: CGFloat = 0,
		var isLastMulti = false
		for i in 0..<items.count {
			let layer 	 = layers[i]
			let item  	 = items[i]

			let isMulti  = item.count > 1
			layer.color  = isMulti ? multiColor : singleColor
			if i != 0 {
				//开始计算位置
				x += isMulti ? maxSpace : isLastMulti ? maxSpace : minSpace
			}
			isLastMulti = isMulti

			layer.position 				= CGPoint(x: x, y: bounds.height / 2 - 10)
			layer.bounds 				= CGRect(x: 0, y: 0, width: 20, height: 20)
			layer.coordinateItem 		= item
			layer.isReverse 			= isReverse
			layer.timeType 				= timeType
			layer.textWidth 			= minSpace
			layer.state 				= item.contains(where: { $0.time = selectedTime }) ? .selected : .normal
		}

		contentSize.width 				= x
		lineLayer?.position 			= CGPoint(x: 0, y: bounds.height / 2 - 10)
		lineLayer?.bounds 				= CGRect(x: 0, y: 0, width: contentSize.width, height: 2)
	}

	@objc fileprivate func didClickView(gestureRecognizer: UITapGestrueRecognizer) {
		let touchPoint 		= gestureRecognizer.location(in: self)
		var selectedLayer: CircleLayer?
		layers.forEach { layer in
			if CGRect (x: layer.frame.minX - 10, y: layer.frame.minY - 10, width: layer.frame.width + 20, height :
				layer.frame.height + 20).contains(touchPoint) {
				selectedLayer = layer
			}
		}

		if selectedLayer != nil {
			selectedTime = selected?.coordinateItem.first?.time
			itemSelectedHandler?(selectedLayer!.coordinateItem)
		}
	}
}



