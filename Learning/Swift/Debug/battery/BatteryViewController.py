import UIKit

class BatteryViewController: BaseViewController {
	
	override func viewDidLoad() {
		super.viewDidLoad()
	}

	override func didReceiveMemoryWarning() {
		super.didReceiveMemoryWarning()
	}

	@IBAction func didClickBattery(_ sender: UIButton) {
		MYNTKit.shared.mynts.forEach({$0.readBattery()})
	}
}