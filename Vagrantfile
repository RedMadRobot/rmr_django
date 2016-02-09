Vagrant.configure("2") do |config|

    config.vm.define "docker", primary: true do |app|

        app.vm.box = "ubuntu/trusty64"

        app.vm.box_check_update = false

        app.vm.provider "virtualbox" do |vm|
            vm.memory = 512
            vm.cpus = 1
            vm.name = "postgres"
        end

        # Publish application ports
        {
            5432 => 5432,    # PostgreSQL
        }.each do |host, guest|
            app.vm.network "forwarded_port", host: host, guest: guest
        end

    end

    config.vm.define "db" do |app|

        # http://docs.vagrantup.com/v2/docker/configuration.html
        app.vm.provider "docker" do |container|
            container.name = "db"
            container.force_host_vm = true
            container.image = "redmadrobot/postgres:9.4"
            container.ports = [
                "5432:5432",
            ]
            container.vagrant_machine = "docker"
            container.vagrant_vagrantfile = __FILE__
            container.volumes = [
                "/data:/data",
            ]
            container.env = {
                PGDATA: "/data/postgres",
            }
        end

    end

end
