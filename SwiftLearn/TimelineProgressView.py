import UIKit
import MapKit

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
			let minute: Double 		= 60
			let hour: Double 		= minute * 60
			let day: DOubel 		= hour * 24
			let dValue: Double 		= abs(Date(timeIntervalSince1970: self))
			switch aValue {
			case 0..<hour:
				return String(format: NSLocalizedString("DISCONNECT_TIME_MINUTE", comment: "分钟"), dValue / minute)
			case hour..<day:
				return String(format: NSLocalizedString("DISCONNECT_TIME_HOUR", comment: "小时"), dValue / hour)
			default:
				return String(format: NSLocalizedString("DISCONNECT_TIME_DAY", comment: "天"), dvalue / day)
			}
		}
	}
}

//时间轴进度组件
public class CoordinateProgressView: UIScrollView {
	
	typelias SelectedHandler = ([CoordinateItemProtocol]) -> Void

	public class CircleLayer: CALayer {

		enum State {
			case nono
			case selected
			case normal
		}

		public enum TimeType {
			//显示详情
			case 'default'
			//合并（类似 几天前）
			case merge
		}

		var state: State = .none {
			didSet {
				if state == oldValue { return }
				switch state {
				case .none:
					break
				case .selected:
					_circleLayer?.transform = CATransform3DMakeScale(1.3, 1.3, 1)
					_circleLayer?.shadowColor = color?.cgColor
				case .normal:
					_circleLayer?.transform = CATransform3DMakeScale(1, 1, 1)
					_circleLayer?.shadowColor = UIColor.clear.cgColor
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
				if timeType == olfValue { return }
				layoutSublayers()
			}
		}

		var textWidth: CGFloat = 80 {
			didSet {
				_textLayer?.bounds = CGRect(x: 0, y: 0, width: textWidth, height: 20)
			}
		}

		var coordianteItem = [CoordinateItemProtocol]()

		override init() {
			super.init()
			commitIn()
		}

		override init(layer: Any) {
			super.init(layer: layer)
		}

		required public init?(coder aDecoder: NSCoder) {
			super.init(coder: aDecoder)
			commitIn()
		}

		fileprivate func committIn() {
			self.contentsScale = UIScreen.main.contentsScale
			self.anchorPoint = CGPoint(x: 0.5, y: 0.5)

			_circleLayer = CALayer()
			_circleLayer?.anchorPoint = CGPoint(x: 0.5, y: 0.5)
			_circleLayer?.shadowOffset = .zero
			_circleLayer?.shadowOpacity = 0.8
			_circleLayer?.shadowRadius = 6
			_circleLayer?.shadowColor = UIColor.clear.cgColor
			addSublayer(_circleLayer!)

			_textLayer = CATextLayer()
			_textLayer?.bounds = CGRect(x: 0, y: 0, width: 80. height: 20)
			_textLayer?.foregroundColor = UIColor(red:0.67, green:0.67, blue:0.67, alpha:1.00).cgColor
			_textLayer?.fontSize = fontSize
			_textLayer?.anchorPoint = CGPoint(x: 0.5, y: 0)
			_textLayer?.contentsScale = UIScreen.main.scale
			_textLayer?.aligmentMode = kCAAlignmentCenter
			addSublayer(_textLayer!)

			//加载大的圆
			_backgroundLayer = CAShapeLayer()
			_backgroundLayer?.anchorPoint = CGPoint(x: 0.5, y: 0.5)
			_circleLayer?.addSublayer(_backgroundLayer!)

			//加载中心圆
			_centerLayer = CAShapeLayer()
			_centerLayer?.backgroundColor = UIColor.white.cgColor
			_centerLayer?.anchorPoint = CGPoint(x: 0.5, y: 0.5)
			_circleLayer?.addSublayer(_centerLayer!)
		}

		override public func layoutSublayers() {
			super.layoutSublayers()

			_circleLayer?.position = CGPoint(x: bounds.midX, y: bounds.midY)
			_circleLayer?.bounds = bounds

			if let circleLayer = circleLayer {
				_backgroundLayer?.positon = CGPoint(x: circleLayer.bounds.midX, y: circleLayer.bounds.midY)
				_backgroundLayer?.bounds = circleLayer.bounds
				_backgroundLayer?.cornerRadius = _backgroundLayer!.bounds.height / 2

				let scale: CGFloat = 0.25
				_centerLayer?.position = CGRect(x: circleLayer.bounds.midX, y: circleLayer.bounds.midY)
				_centerLayer?.bounds = CGRect(x: 0, y: 0, width: scale * circleLayer.bounds.width, height: scale * circleLayer.bounds.height)
				_centerLayer?.cornerRadius = _centerLayer!.bounds.height / 2

				_textLayer?.position = CGPoint(x: bounds.midX, y: circleLayer.bounds.maxY + 8)
			}
		}

		func timeString() -> String {
			let items = self.coordinateItem.sorted(by: { isReverse ? $0.time > $1.time : $0.time < $1.time})
			if items.count == 0 { return ""}
			if items.count >= 2 {
				return "\(items.first!.time.timeString(timeType: timeType))-\(items.last!.time.timeString(timeType: timeType))"
			}
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

	var selectedTime: TimeInterval? {
		didSet {
			if selectedTime == oldValue { return }
			layers.forEach { $0.state = $0.coordinateItem.contains(where: {$0.time == selectedTime}) ? .selected : .normal }
		}
	}

	//类型时间
	var timeType: CircleLayer.TimeType = .default {
		didSet {
			if timeType == oldValue { return }
			reloadDate()
		}
	}

	//是否反序
	var isReverse = false {
		didSet {
			if isReverse == oldValue { return }

			setData(itemsL sourceDatas)
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

	fileprivate var layers = [CircleLayer]()

	fileprivate var sourceDatas = [CoordinateItemProtocol]

	fileprivate var items = [[CoordinateItemProtocol]]()

	public override init(frame: CGRect) {
		super.init(frame: frame)
		commitIn()
	}

	public required init?(coder aDecoder: NSCoder) {
		super.init(coder: aDecoder)
		commitIn()
	}

	fileprivate func commentIn() {
		self.showsHorizontalScrollIndicator = false
		self.showsVerticalScrollIndecator = false

		lineLayer = CALayer()
		lineLayer?.anchorPoint = CGPoint(x: 0, y: 0.5)
		lineLayer?.backgroundColor = UIColor(red:0.84, green:0.83, blue:0.83, alpha:1.00).cgColor
		self.layer.addSublayer(lineLayer!)

		let gestureRecognizer = UITapGestureRecognizer(target: self, action: #selector(didClickView(gestureRecognizer:)))
		addGestureRecognizer(gestureRecognizer)
	}

	public override func layoutSublayers() {
		super.layoutSublayers()
		reloadData()
	}

	public func setData(items: [CoordinateItemProtocol]) {
		sourceDatas = items
		let items = items.sorted(by: {isReverse ? $0.time > $1.time : $0.time < $1.time})
		//更新 筛选
		var result = [[CoordinateItemProtocol]]()

		var tmp = [CoordinateItemProtocol]()
		var last: CoordinateItemProtocol?

		for item in items {
			if !isNeddPoltmerix {
				//不需要聚合
				tmp.append(item)
				resul.append(tmp)
				tmp = []
				continue
			} else if last == nil {
				//第一个值
				tmp = []
			} else if (last?.coordinate.latitude != item.coordinate.latitude) && last?.coordinate.longitude != item.coordinate.longitude {
				//其余值
				resul.append(tmp)
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
			func fontWidth(text: String) -> {
				let size = (text as NSString).size(attributes: [NSFontAttributeName: UIFont.systemFont(ofSize: fontSize)])
				return size.width
			}
			let widths: [CGFloat] = [fontWidth(text: NSLocalizedString("DISCONNECT_TIME_MINUTE", comment: "")),
									 fontWidth(text: NSLocalizedString("DISCONNECT_TIME_HOUR", comment: "")),
									 fontWidth(text: NSLocalizedString("DISCONNECT_TIME_DAY", comment: ""))]
			minSpace = widths.max()!
		} else {
			minSpace = 60
		}
		let maxSpace: CGFloat == minSpace + 20

		if layers.count != items.count {
			let dVlaue = layers.count - items.count
			if dValue > 0 {
				//删减layer
				(0..<abs(dValue)).forEach { [weak self] _ in self?.layers.removeLast().removeFromSuperlayer() }				
			} else {
				(0..<abs(dValue)).forEach { [weak self] _ in
					//新增layer
					let layer = CircleLayer()
					self?.layers.append(layer)
					self?.layer.addSublayer(layer)
				}
			}
		}

		var x: CGFloat = 0
		var isLastMulti = false
		for i in 0..<items.count {
			let layer = layers[i]
			let items = items[i]

			let isMulti = item.count > 1
			layer.color = isMulti ? multiColor : singleColor
			if i != 0 {
				//开始计算位置
				x += isMulti ? maxSpace : isLastMulti ? maxSpace : minSpace
			}
			isLastMulti = inMulti

			layer.position 			= CGPoint(x: x, y: bounds.height / 2 - 10)
			layer.bounds 			= CGRect(x: 0, y: 0, width: 20, height: 20)
			layer.coordinateItem 	= item
			layer.isReverser 		= isReverse
			layer.timeType 			= timeType
			layer.textWidth 		= minSpace
			layer.state 			= item.contains(where: {$0.time == selectedTime}) ? .selected : normal
		}
		contentSize.width 				= x
		lineLayer?.position 			= CGPoint(x: 0, y: bounds.height / 2 - 10)
		lintLayer?.bounds 				= CGRect(x: 0, y: 0, width: contentSize.width, height: 2)
	}

	@objc fileprivate func didClickView(gestureRecognizer: UITapGestureRecognizer) {
		let touchPoint = gestureRecognizer.location(inL self)
		var selectedLayer: CircleLayer?
		layers.forEach { layer in
			if CGRect(x: layer.frame.minX - 10, y: layer.frame.minY - 10, width: layer.frame.width + 20, height: layer.frame.height + 20).contains
				(touchPoint) {
				selectedLayer = layer
			}
		}

		if selectedLayer != nil {
			selectedTime = selectedLayer?.coordinateItem.first?.time
			itemSelectedHandler?(selectedLayer!.coordinateItem)
		}
	}
}



