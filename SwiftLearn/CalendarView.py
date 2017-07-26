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

		layout = UICollectionViewFlowLayout()
		layout.scrollDirection = .herizontal
		collectionView = UICollectionView(frame: .zero, collectionViewLayout: layout)
		collectionView?.backgroundColor = .clear
		collectionView?.delegate = self
		collectionView?.dataSource = self
		collectionView?.isPagingEnabled = true
		collectionView?.translatesAutoresizingMaskIntoConstraints = false
		collectionView.showsVerticalScrollIndicator = false
		collectionView.showsHorizontalScrollIndicator = false
		collectionView.layer.masksToBounds = false
		collectionView?.register(CalendarCollectionViewCell.self, forCellWithReuseIdentifier: "CalendarCollectionViewCell")
		addSubview(collectionView!)
		updateCollectionViewConstraints()
	}

	public override func layoutSubviews() {
		super.layoutSubviews()

		updateCollectionViewConstraints()
		let width = (UIScreen.main.bounds.width - bounds.height) / 7
		layout.itemSize = CGSize(width: width, height: bounds.height)
		layout.minimumLineSpacing = 0.01
		layout.minimumInteritemSpacing = 0.01
		layout.sectionInset = UIEdgeInsetsMake(0, 0, 0, 0)

		collectionView?.layoutIfNeeded()
		collectionView?.setNeedsLayout()
		collectionView?.setContentOffset(CGPoint(x: collectionView.contentSize.width - collectionView.frame.width, y: 0), animated: false)
	}

	fileprivate func updateCollectionViewConstraints() {
		if collectionView == nil { return }
		collectionView.removeConstraints(widthConstraints)
		collectionView.removeConstraints(heightConstraints)

		widthConstraints = NSLayoutConstraint.constraints(withVisualFormat: "H:|-(d)-[view]-(d)-|",
														  options: .directionLeftToRight,
														  metrics: ["d": bounds.height / 2],
														  views: ["view": collectionView!])
		heightConstraints = NSLayoutConstraint.constraints(withVisualFormat: "V:|-0-[view]-0-|",
														   options: .directionLeftToRight,
														   metrics: ["d": bounds.height / 2],
														   views: ["view": collectionView!])
		addConstraints(widthConstraints)
		addConstraints(heightConstraints)
	}

	public func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
		return dates.count
	}

	public func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
		let cell = collectionView.dequeueReusableCell(withReuseIdentifier: "CalendarCollectionViewCell", for: indexPath) as? CalendarCollectionViewCell
		let date = dates[indexPath.row]
		cell?.label?.text = "\(date.dayString)"
		cell?.label?.backgroundColor = selectedDate == date ? UIColor(red:0.24, green:0.56, blue:1.00, alpha:1.00) : .clear
		cell?.label?.textColor = selectedDate == date ? .white : date.timeIntervalSince1970 > todayDate.timeIntervalSince1970 ? UIColor(red:0.77, green:0.77, blue:0.77, alpha:1.00) : .black
		return cell!
	}

	public func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
		let date = dates[indexPath.row]
		if date.timeIntervalSince1970 > todayDate.timeIntervalSince1970 { return }
		selectedDate = date
		collectionView.reloadDate()

		delegate?.didSelectDay(calendarView: self, date: date)
	}
}

