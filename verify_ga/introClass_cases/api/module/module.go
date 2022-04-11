package module




type Info struct {
	AllStudents []*Student `json:"all_students"`
}

type Student struct {
	StuValue string `json:"value"`
	StuName string `json:"label"`
	Jobs []*Job `json:"children"`
}
type Job struct {
	JobValue string `json:"value"`
	JobName string `json:"label"`
}
func (st *Student) AppendJob(jobName string,jobValue string) {
	st.Jobs = append(st.Jobs, &Job{
		JobName: jobName,
		JobValue: jobValue,
	})
}

func (info *Info) AppendStudent(stu *Student) {
	info.AllStudents = append(info.AllStudents, stu)
}