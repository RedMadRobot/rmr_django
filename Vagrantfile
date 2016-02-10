Vagrant.configure("2") do |config|

    config.vm.define "docker", primary: true do |app|

        app.vm.box = "ubuntu/trusty64"

        app.vm.provider "virtualbox" do |vm|
            vm.memory = 1024
            vm.cpus = 2
            vm.name = "rmr"
        end

        # Publish application ports
        {
            5432 => 5432,    # PostgreSQL
            5672 => 5672,    # RabbitMQ
            15672 => 15672,  # RabbitMQ management
        }.each do |host, guest|
            app.vm.network "forwarded_port", host: host, guest: guest
        end

        # install Docker
        app.vm.provision "docker"

    end

    config.vm.define "postgres" do |app|

        # http://docs.vagrantup.com/v2/docker/configuration.html
        app.vm.provider "docker" do |container|
            container.name = "postgres"
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

    config.vm.define "rabbitmq" do |app|

        # http://docs.vagrantup.com/v2/docker/configuration.html
        app.vm.provider "docker" do |container|
            container.name = "rabbitmq"
            container.force_host_vm = true
            container.image = "rabbitmq:3-management"
            container.ports = [
                "5672:5672",
                "15672:15672",  # admin web interface
            ]
            container.vagrant_machine = "docker"
            container.vagrant_vagrantfile = __FILE__
            container.volumes = [
                "/data:/var/lib",
            ]
            container.env = {
                RABBITMQ_DEFAULT_USER: "rabbitmq",
                RABBITMQ_DEFAULT_PASS: "rabbitmq",
            }
        end

    end

end
