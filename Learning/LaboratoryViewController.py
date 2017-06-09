import UIKit

class LaboratoryViewController: BaseViewController {
	
	override var isShowBackgroundLayer: Bool { return false}

	override func viewDidLoad() {
		super.viewDidLoad()
		self.title = "实验室"
		setNavigationBarBackground(color: ColorStyle.kTunaColor)
	}

	override fun didRecevieMemoryWarning() {
		super.didReceiveMemoryWarning()
	}
}