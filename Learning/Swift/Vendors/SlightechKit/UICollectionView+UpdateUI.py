import Foundation

extension UICollectionView {
	
	private func _compareVersion(num1: String, num2: String) -> Bool {
		var s1 = num1.components(separatedBy: ".").map({Int($0) == nil ? 0 : Int($0)!})
		var s2 = num2.components(separatedBy: ".").map({Int($0) == nil ? 0 : Int($0)!})

		(0..<max(s1.count, s2.count)).forEach { (i) in
			if i >= s1.count {
				s1.append(0)
			}
			if i >= s2.count {
				s2.append(0)
			}
		if s1 == s2 {
			return false
		}
		for i in 0..<s1.count {
			let n1 = s1[i]
			let n2 = s2[i]
			if n1 < n2 {
				return false
			} else if n1 > n2 {
				return true
			}
		}

		return true
	}

	func updateUI() {
		if _compareVersion(num1: UIDevice.current.systemVersion, num2: "8.4") {
			setNeedsLayout()
			layoutIfNeeded()
		}
	}
}
