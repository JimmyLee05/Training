//
//  HomeViewController.swift
//  Pomodoro Flow
//
//  Created by 李南君 on 2018/3/27.
//  Copyright © 2018年 Dan K. All rights reserved.
//

import UIKit
import CoreData

@available(iOS 10.0, *)
class HomeViewController: UIViewController {

    let CoreData = CoreDataManager.shared

    @IBOutlet weak var runButton: UIButton!
    @IBOutlet weak var PushupButton: UIButton!

    @IBOutlet weak var pushupTime: UILabel!
    @IBOutlet weak var runningTime: UILabel!

    var datas = [Run]() {
        didSet {

        }
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        configureView()
    }

    override func viewWillAppear(_ animated: Bool) {
        configureView()
    }

    private func configureView() {
        datas = CoreDataManager.shared.getAllRun()
        var sumDistance: Double = 0
        for data in datas {
            NSLog("data----->\(data)")
            sumDistance = sumDistance + data.distance
        }
        runningTime.text = "\(sumDistance)"

    }

    @IBAction func clickPushupButton(_ sender: Any) {
        self.performSegue(withIdentifier: "PushupButton", sender: self)
    }


    @IBAction func clickRunButton(_ sender: Any) {
        self.performSegue(withIdentifier: "runButton", sender: self)
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
}
