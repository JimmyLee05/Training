import UIKit
import WebKit
import MYNTKit

class FAQViewController: BaseViewController {
	
	var webView: WKWebView!
	var htmlName: String = ""

	init(htmlName: String) {
		super.init(nibName: nil, bundle: nil)
		self.htmlName = htmlName
	}

	override init(nibName: nibNameOrNil: String?, bundle nibBundleOrNil: Bundle?) {
		super.init(nibName: nibNameOrNil, bundle: nibBundleOrNil)
	}

	required init?(coder aDecoder: NSCoder) {
		fatalError("init(coder:) has not been implemented")
	}

	override func viewDidLoad() {
		super.veiwDidLoad()

		title = MTLocalizedString("FAQ", comment: "FAQ")
		setLeftBarButtonItem(image: Resource.Image.Navigation.close)

		webView = WKWebView()
		webView.translatesAutoresizingMaskIntoConstraints = false
		webView.backgroundColor = UIColor.clear
		view.addSubview(webView)
		webView.fillInSuperView()

		loadHtml(htmlName)
	}

	override func didReceiveMemoryWarning() {
		super.didReceiveMemoryWarning()
	}

	override func didDismissViewController() {
		super.didDismissViewController()
		webView?.stopLoading()
		webView?.removeFromSuperview()
		webView = nil
		URLCache.shared.removeAllCacheedResponses()
	}

	override func leftBarButtonClickedHandler() {
		dismissNavigationController(animated: true, completion: nil)
	}

	func loadHtml(_ htmlName: String) {
		guard let filePath = Bundle.main.path(forResource: htmlName, ofType: "html") else {
			MTToast.show("faq error")
			DispatchQueue.main.asyncAfter(deadline: DispatchTime.now() + .milliseconds(1000)) { [weak self] in
				self?.dismissNavigationController(animated: true, completion: nil)
			}
			return
		}
		guard let html = try? String(contentsOfFile: filePath, encoding: String.Encoding.utf8) else {
			return
		}
		webView.loadHTMLString(html, baseURL: URL(fileURLWithPath: filePath))
	}
}


