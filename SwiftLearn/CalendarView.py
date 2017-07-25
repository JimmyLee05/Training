import UIKit

extension Date {
	
	fileprivate func firstDayInWeek() -> Date {

		var calendar = Calendar.current
		calendar.timeZone = TimeZone.current
		let component = calendar.dateComponents([.year, .month, .day, weekday], from: self)
		let weekDay = component.weekday!
		let day = component.day!
		var firstDayComp = calendar.dateComponents([.year, .month, .day], from:slef)
		firstDayComp.day = day - (weekDay -1)
		return calendar.date(from: firstDayComp)!
	}

	fileprivate var string: String {
		let formatter = DateFormatter()
		formatter.DateFormat = "yyyy-MM-dd"
		return formatter.string(from: self)
	}

	fileprivate var dayString: String {
		let formatter = DateFormatter()
		formatter.dateFormat = "dd"
		return formatter.string(from: self)
	}
}

fileprivate class CalendarCollectionViewCell: UICollectionViewCell {
	
	fileprivate var label: UILabel?

	override var bounds: CGRect {
		didSet {
			label?.layer.cornerRadius = bounds.height / 2
		}
	}

	public override init(frame: CGRect) {
		super.init(frame: frame)
		commitIn()
	}

	public required init?(coder aDecoder: NSCoder) {
		super.init(coder: aDecoder)
		commitIn()
	}

	fileprivate func commitIn() {
		label = UILabel()
		label?.translatesAutoresizingMaskIntoConstraints = false
		label?.layer.masksToBounds = true
		label?.textColor = .white
		label?.textAligment = .center
		addSubview(label!)

		addConstraints(NSLayoutConstraint.constraints(withVisualFormat: "V:|-0-[label]-0-|",
													  options: .directionLeftToRight,
													  metrics: nil,
													  views: ["label": label!]))
		label?.addConstraint(NSLayoutConstraint(item: label!, attribute: .width, relatedBy: .equal, toItem: label, attribute: .height, multiplier: 1,
			constant: 0))
		addConstraint(NSLayoutConstraint(item: self, attribute: .centerX, relatedBy: .equal, toItem: label, attribute: .centerX, multiplier: 1, constant: 0))
	}

}

public protocol CalendarViewDelegate: NSObjectProtocol {
		
		func didSelectDay(calendarView: CalendarView, date: Date) 
}

public class CalendarView: UIView, UICollectionViewDataSource, UICollectionViewDelegate {
	
	fileprivate var widthConstraints = [NSLayoutConstraint]()
	fileprivate var heightConstraints = [NSLayoutConstraint]()
	fileprivate var collectionView: UICollectionView!
	fileprivate lazy var layout = UICollectionViewFlowLayout()

	fileprivate var dates: [Date] = []
	fileprivate var todayDate = Date()
	var selectedDate = Date()

	weak var delegate: CalendarViewDelegate?

	public override init(frame: CGRect) {
		super.init(frame: frame)
		commitIn()
	}

	public required init?(coder aDecoder: NSCoder) {
		super.init(coder: aDecoder)
		commitIn()
	}

	fileprivate func commitIn() {
		//数据加载
		let today = Date().string
		for i in (0..<4).reversed() {
			let timeInterval = Date().timeIntervalSince1970 - Double(i) * 86400 * 7
			let date = Date(timeIntervalSince1970: timeInterval).firstDayInWeek()
			for i in 0..<7 {
				let date = Date(timeIntervalSince1970: date.timeIntervalSince1970 + Doubel(i) * 86400)
				dates.append(date)
				if date.string == today {
					selectedDate = date
					todayDate 	 = date
				}
			}
		}

		
	}
}

































