# -*- mode: ruby -*-
# vi: set ft=ruby :
servers = {
  "producer" => { :ip => "192.168.56.2", :cpus => 1, :mem => 1024, :ssh_port=>2222 },
  "consumerA" => { :ip => "192.168.56.3", :cpus => 1, :mem => 1024, :ssh_port=>2222 },
  "consumerB" => { :ip => "192.168.56.4", :cpus => 1, :mem => 1024, :ssh_port=>2222 },

  
}
Vagrant.configure("2") do |config| #Loads the Vagrant API version 2 and assign to variable config
  servers.each_with_index do |(hostname, info), index|
     config.vm.define hostname do |cfg|

       cfg.vm.provider :virtualbox do |vb, override| 
         config.vm.box = "bento/ubuntu-19.10"
         override.vm.network "private_network", ip: "#{info[:ip]}"
         #Fix SSH forwarded port
         override.vm.network "forwarded_port", guest: 22, host:"#{info[:ssh_port]}", id: "ssh", auto_correct: true
         override.vm.hostname = hostname
         vb.name = hostname
         
         override.vm.provision "file", source: "~/.ssh/id_rsa.pub", destination: "/home/vagrant/.ssh/public_key"
         override.vm.provision "shell", inline: "cat /home/vagrant/.ssh/public_key >> /home/vagrant/.ssh/authorized_keys"
         override.vm.provision "shell", inline: "rm /home/vagrant/.ssh/public_key"
         vb.name = hostname
       end
     end
  end
  #provision for servers
    config.vm.provision "ansible" do |ansible|
            ansible.inventory_path = 'hosts'
            ansible.verbose = 'vvv'
            ansible.playbook = 'playbooks/servers.yml'
#            ansible.limit = 'all'
    end
end
