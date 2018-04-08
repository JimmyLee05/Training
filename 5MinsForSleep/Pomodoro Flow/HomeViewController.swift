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

    @IBOutlet weak var pushupTime: UILabel!
    @IBOutlet weak var runningTime: UILabel!

    var distanceDatas = [Run]() {
        didSet {
        }
    }

    var timesDatas = [Pushup]() {
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

        distanceDatas = CoreDataManager.shared.getAllRun()
        var sumDistance: Double = 0
        
        for data in distanceDatas {
            NSLog("data----->\(data)")
            sumDistance = sumDistance + data.distance
        }
        let string = String(format: "%.2f", sumDistance)
        runningTime.text = "\(string)"

        timesDatas = CoreDataManager.shared.getAllPushup()
        var sumTimes: Double = 0

        for data in timesDatas {
            NSLog("data----->\(data)")
            sumTimes = sumTimes + data.time
        }
        let stirng = String(format: "%.0f", sumTimes)
        pushupTime.text = "\(stirng)"
    }



    @IBAction func clickPushupButton(_ sender: Any) {
        self.performSegue(withIdentifier: "pushup", sender: self)
    }


    @IBAction func clickRunButton(_ sender: Any) {
        self.performSegue(withIdentifier: "run", sender: self)
    }

    @IBAction func CrashButton(_ sender: Any) {
        NSLog("Test crash");
        let array = [1, 2]
        print(array[3])
    }


    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
}
