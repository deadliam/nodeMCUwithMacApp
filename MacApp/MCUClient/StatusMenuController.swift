//
//  StatusMenuController.swift
//  MCUClient
//
//  Created by Anatoly Kasyanov on 2/14/19.
//

import Foundation
import Cocoa

class StatusMenuController: NSObject {
    
    enum door: String {
        case Open = "Open"
        case Closed = "Closed"
    }
    
    let status = StatusAPI()
    
    let isOpen = true

    @IBOutlet weak var menu: NSMenu!
    
    override init() {
        super.init()
        Timer.scheduledTimer(timeInterval: 5.0, target: self, selector: #selector(updateStatus), userInfo: nil, repeats: true)
    }
    
    let statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.variableLength)
    
    @objc func updateStatus() {
        status.makeGetCall { success in
            DispatchQueue.main.async {
                self.statusItem.button?.title = success == "true" ? door.Open.rawValue :  door.Closed.rawValue
            }
        }
    }
    
    @IBAction func quitClicked(sender: NSMenuItem) {
        NSApplication.shared.terminate(self)
    }
    
    @IBAction func updateClicked(_ sender: NSMenuItem) {
        updateStatus()
    }
}
