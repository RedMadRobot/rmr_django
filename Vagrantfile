Vagrant.configure("2") do |config|

    config.vm.define "docker", primary: true do |app|

        app.vm.box = "ubuntu/trusty64"

        app.vm.box_check_update = false

        app.vm.provider "virtualbox" do |vm|
            vm.memory = 1024
            vm.cpus = 2
            vm.name = "rmr"
        end

        # Publish application ports
        {
            5432 => 5432,    # PostgreSQL 9.4
            5433 => 5433,    # PostgreSQL 9.5
            5672 => 5672,    # RabbitMQ
            15672 => 15672,  # RabbitMQ management
        }.each do |host, guest|
            app.vm.network "forwarded_port", host: host, guest: guest
        end

        # build Docker images
        app.vm.provision "docker" do |docker|
            docker.build_image "/vagrant/etc/postgres/9.4", args: "--tag=redmadrobot/postgres:9.4"
            docker.build_image "/vagrant/etc/postgres/9.5", args: "--tag=redmadrobot/postgres:9.5"
        end

        # remove obsolete Docker images
        app.vm.provision "shell",
            inline: "docker images | sed 1d | grep '<none>' | awk '{print($3)}' | uniq | xargs docker rmi || true"

    end

    config.vm.define "postgres-9.4" do |app|

        # http://docs.vagrantup.com/v2/docker/configuration.html
        app.vm.provider "docker" do |container|
            container.name = "postgres-9.4"
            container.force_host_vm = true
            container.image = "redmadrobot/postgres:9.4"
            container.ports = [
                "5432:5432",
            ]
            container.vagrant_machine = "docker"
            container.vagrant_vagrantfile = __FILE__
            container.volumes = [
                "/data/postgres:/data/postgres",
            ]
            container.env = {
                PGDATA: "/data/postgres/9.4",
            }
        end

    end

    config.vm.define "postgres-9.5" do |app|

        # http://docs.vagrantup.com/v2/docker/configuration.html
        app.vm.provider "docker" do |container|
            container.name = "postgres-9.5"
            container.force_host_vm = true
            container.image = "redmadrobot/postgres:9.5"
            container.ports = [
                "5433:5432",
            ]
            container.vagrant_machine = "docker"
            container.vagrant_vagrantfile = __FILE__
            container.volumes = [
                "/data/postgres:/data/postgres",
            ]
            container.env = {
                PGDATA: "/data/postgres/9.5",
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
                "/data/rabbitmq:/var/lib/rabbitmq",
            ]
            container.env = {
                RABBITMQ_DEFAULT_USER: "rabbitmq",
                RABBITMQ_DEFAULT_PASS: "rabbitmq",
            }
        end

    end

end
